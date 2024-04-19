import hmac
import logging
import time
from base64 import b64encode
from hashlib import sha256
from typing import List, Callable, Optional
from warnings import warn

from pydantic import BaseModel, computed_field

from . import errors as err
from . import models
from .methods import GetUser, CreatePayment, CreateTransaction, GetSelfCardInfo, SetTransactionWebhook, GetMe, \
    GetUserCards


class AuthorizationPair(BaseModel):
    id: str
    token: str

    @computed_field
    @property
    def authorization(self) -> str:
        return f'Bearer ' + str(b64encode(str(f'{self.id}:{self.token}').encode('utf-8')), 'utf-8')

    def verify_webhook(self, webhook_data: str, X_Body_Hash: str):
        hmac_data = hmac.new(self.token.encode('utf-8'), webhook_data.encode('utf-8'), sha256).digest()
        base64_data = b64encode(hmac_data)
        return hmac.compare_digest(base64_data, X_Body_Hash.encode('utf-8'))


class SpApi:
    """
    **API класс для работы с spworlds api**

    :param card_id: Индефикатор карты
    :type card_id: str

    :param card_token: Секретный ключ доступа карты
    :type card_token: str
    """

    def __init__(self, card_id: str, card_token: str):
        self._auth = AuthorizationPair(
            id=card_id,
            token=card_token
        )

    def ping(self) -> bool:
        """
            Проверка работоспособности API.

            :return: Состояние API.
        """
        try:
            self.card()
            return True

        except err.SpwApiError:
            return False

    def get_user(self, discord_id: str) -> models.User:
        """
            Получение пользователя.

            :param discord_id: ID пользователя дискорда.
            :type discord_id: bool

            :return: Объект пользователя.

            :raises SpwUserNotFound: Пользователь не был найден.
        """

        try:
            return GetUser(
                discord_id=int(discord_id)
            )(self._auth.authorization)

        except err.SpwApiError as e:
            if e.status_code == 404:
                raise err.SpwUserNotFound(discord_id)

            raise e

    def check_access(self, discord_id: str) -> bool:
        """
            Получение статуса проходки.

            :param discord_id: ID пользователя дискорда.
            :type discord_id: bool

            :return: Состояние проходки пользователя.
        """

        try:
            GetUser(
                discord_id=int(discord_id)
            )(self._auth.authorization)
            return True

        except err.SpwApiError as e:
            if e.status_code == 404:
                return False

            raise e

    def check_webhook(self, webhook_data: str, X_Body_Hash: str) -> bool:
        """
            Валидирует webhook.

            :param webhook_data: Тело webhook'а.
            :type webhook_data: str

            :param X_Body_Hash: Хэдер X-Body-Hash из webhook.
            :type X_Body_Hash: str

            :return: Верефецирован или нет вебхук.
        """

        return self._auth.verify_webhook(webhook_data, X_Body_Hash)

    def create_payment(self, payment: models.Payment) -> str:
        """
            Создание ссылки на оплату.

            :param payment: Параметры оплаты.
            :type payment: Payment

            :return: Ссылку на страницу оплаты, на которую стоит перенаправить пользователя.
        """

        return CreatePayment(
            payment=payment
        )(self._auth.authorization).url

    def send_transaction(self, transaction: models.Transaction):
        """
            Отправка транзакции.
            
            :param transaction: Параметры транзакции.
            :type transaction: Transaction

            :raises SpwInsufficientFunds: Недостаточно средств на карте.
            :raises SpwCardNotFound: Карта получателя не найдена.
        """

        try:
            CreateTransaction(
                transaction=transaction
            )(self._auth.authorization)

        except err.SpwApiError as e:
            if e.status_code == 400:
                if e.extra_info == 'Недостаточно средств на карте':
                    raise err.SpwInsufficientFunds()

                elif e.extra_info == 'Карты не существует':
                    raise err.SpwCardNotFound()

            raise e

    def card(self) -> models.SelfCard:
        """
            Получение информации о токен-карте.

            :return: Card класс с информации о карте.
        """

        return GetSelfCardInfo()(self._auth.authorization)

    def get_balance(self) -> int:
        """
            Получение баланса.

            :return: Значения баланса карты.
        """
        warn('Use .card().balance', DeprecationWarning)

        return self.card().balance

    def set_transaction_webhook(self, url: Optional[str]):
        """
            Установка адреса для получения вебхуков о транзакциях по карте.

            :param url: Адрес вебхука.
            :type url: Optional[str]
        """

        SetTransactionWebhook(
            url=url
        )(self._auth.authorization)

    def me(self) -> models.SelfUser:
        """
            Получения пользователя владельца карты.

            :return: Пользователь владельца карты.
        """

        return GetMe()(self._auth.authorization)

    def get_user_cards(self, username: str) -> List[models.Card]:
        """
            Получения карта пользователя.

            :param username: Имя пользователя у которого надо получить карты.
            :type username: str

            :return: Список карт пользователя.
        """

        return GetUserCards(
            username=username
        )(self._auth.authorization)

    # ---------------------------------
    # ------------- Manys -------------
    # ---------------------------------

    def _many_req(self, iterable: List, method: Callable, delay: float) -> List:
        users = []

        if len(iterable) > 100 and delay <= 0.5:
            logging.warning('You send DOS attack to SPWorlds API. Please set the delay to greater than to 0.5')

        for i in iterable:
            users.append(method(i))
            time.sleep(delay)

        return users

    def get_users(self, discord_ids: List[str], delay: float = 0.3) -> List[models.User]:
        """
            Получение пользователей.

            :param delay: Значение задержки между запросами, указывается в секундах.
            :type delay: float

            :param discord_ids: Список discord id пользователей, которых вы бы хотели получить.
            :type discord_ids: List[str]

            :return: Список с пользователями.

            :raises SpwUserNotFound: Пользователь не был найден.
        """
        return self._many_req(discord_ids, self.get_user, delay)

    def check_accesses(self, discord_ids: List[str], delay: float = 0.3) -> List[bool]:
        """
            Получение статуса проходок.

            :param delay: Значение задержки между запросами, указывается в секундах.
            :type delay: float

            :param discord_ids: Список discord id пользователей статусы проходок, которых вы бы хотели получить.
            :type discord_ids: List[str]

            :return: Список со статусами проходок.
        """
        return self._many_req(discord_ids, self.check_access, delay)

    def create_payments(self, payments: List[models.Payment], delay: float = 0.5) -> List[str]:
        """
            Создание ссылок на оплату.

            :param delay: Значение задержки между запросами, указывается в секундах.
            :type delay: float

            :param payments: Список параметров оплаты.
            :type payments: List[Payment]

            :return: Список ссылок на оплату.
        """
        return self._many_req(payments, self.create_payment, delay)

    def send_transactions(self, transactions: List[models.Transaction], delay: float = 0.5, safe: bool = True) -> None:
        """
            Отправка транзакций.

            .. warning::
                **Важно: Если safe=true, то перед множетсвенной отправки транзаций проводится дополнительная проверка на количество средств на карте.
                В случае если во время совершения транзакций кто-либо еще спишет с этой карты сумму, после которой
                остаток на карте не будет достаточен для проведения транзакции, то выполнение транзакций прервется,
                а предыдущие транзации не откатятся.**

            :param safe: Значение задержки между запросами, указывается в секундах.
            :type safe: bool

            :param delay: Значение задержки между запросами, указывается в секундах.
            :type delay: float

            :param transactions: Список параметров транзакций
            :type transactions: List[Transaction]

            :raises SpwInsufficientFunds: Недостаточно средств на карте.
            :raises SpwCardNotFound: Карта получателя не найдена.
        """

        # Additional balance verify
        if safe and self.card().balance < sum([tr.amount for tr in transactions]):
            raise err.SpwInsufficientFunds()

        self._many_req(transactions, self.send_transaction, delay)
