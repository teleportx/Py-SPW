import json
import platform
from base64 import b64encode
from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import hmac
import requests as rq
import time
from typing import List, Callable
import logging
from mojang import API as MAPI

from . import errors as err
from . import models

mapi = MAPI()


class _RequestTypes(Enum):
    POST = 'POST'
    GET = 'GET'


@dataclass
class _Card:
    id: str
    token: str


class SpApi:
    """
    API класс для работы с spworlds api

    :param card_id: Индефикатор карты
    :type card_id: str

    :param card_token: Секретный ключ доступа карты
    :type card_token: str
    """

    _spworlds_api_url = 'https://spworlds.ru/api/public'

    def __init__(self, card_id: str, card_token: str):
        self._card = _Card(card_id, card_token)
        self._authorization = f"Bearer {str(b64encode(str(f'{card_id}:{card_token}').encode('utf-8')), 'utf-8')}"

    def _request(self, method: _RequestTypes, path: str = '', body: dict = None, *,
                 ignore_codes=None) -> rq.Response:
        if ignore_codes is None:
            ignore_codes = []

        headers = {
            'Authorization': self._authorization,
            'User-Agent': f'Py-SPW (Python {platform.python_version()})'
        }
        try:
            response = rq.request(method.value, url=self._spworlds_api_url + path, headers=headers, json=body)

        except rq.exceptions.ConnectionError as error:
            raise err.SpwApiError(error)

        if response.headers.get('Content-Type') != 'application/json':
            raise err.SpwApiDDOS()

        if response.ok or response.status_code in ignore_codes:
            return response

        elif response.status_code == 401:
            raise err.SpwUnauthorized()

        elif response.status_code >= 500:
            raise err.SpwApiError(f'HTTP: {response.status_code}, Server Error.')

        else:
            raise err.SpwApiError(
                f'HTTP: {response.status_code} {response.json()["error"]}. Message: {response.json()["message"]}')

    def ping(self) -> bool:
        """
            Проверка работоспособности API.

            :return: Состояние API.
        """
        try:
            self.get_balance()
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

        response = self._request(_RequestTypes.GET, f'/users/{discord_id}', ignore_codes=[404])
        if response.status_code == 404:
            raise err.SpwUserNotFound(discord_id)

        return models.User(response.json()['username'])

    def check_access(self, discord_id: str) -> bool:
        """
            Получение статуса проходки.

            :param discord_id: ID пользователя дискорда.
            :type discord_id: bool

            :return: Состояние проходки пользователя.
        """
        response = self._request(_RequestTypes.GET, f'/users/{discord_id}', ignore_codes=[404])
        return response.status_code != 404

    def check_webhook(self, webhook_data: str, X_Body_Hash: str) -> bool:
        """
            Валидирует webhook.

            :param webhook_data: Тело webhook'а.
            :type webhook_data: str

            :param X_Body_Hash: Хэдер X-Body-Hash из webhook.
            :type X_Body_Hash: str

            :return: Верефецирован или нет вебхук.
        """

        hmac_data = hmac.new(self._card.token.encode('utf-8'), webhook_data.encode('utf-8'), sha256).digest()
        base64_data = b64encode(hmac_data)
        return hmac.compare_digest(base64_data, X_Body_Hash.encode('utf-8'))

    def create_payment(self, payment: models.Payment) -> str:
        """
            Создание ссылки на оплату.

            :param payment: Параметры оплаты.
            :type payment: Payment

            :return: Ссылку на страницу оплаты, на которую стоит перенаправить пользователя.
        """
        return self._request(_RequestTypes.POST, '/payment', payment.model_dump()).json()['url']

    def send_transaction(self, transaction: models.Transaction) -> None:
        """
            Отправка транзакции.
            
            :param transaction: Параметры транзакции.
            :type transaction: Transaction

            :raises SpwInsufficientFunds: Недостаточно средств на карте.
            :raises SpwCardNotFound: Карта получателя не найдена.
        """
        response = self._request(_RequestTypes.POST, '/transactions', transaction.model_dump(), ignore_codes=[400])
        if response.status_code == 400:
            msg = response.json()["message"]
            if msg == 'Недостаточно средств на карте':
                raise err.SpwInsufficientFunds()

            elif msg == 'Карты не существует':
                raise err.SpwCardNotFound()

    def get_balance(self) -> int:
        """
            Получение баланса.

            :return: Значения баланса карты.
        """
        return self._request(_RequestTypes.GET, '/card').json()['balance']

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

    def send_transactions(self, transactions: List[models.Transaction], delay: float = 0.5) -> None:
        """
            Отправка транзакций.

            .. warning::
                **Важно: Перед множетсвенной отправки транзаций проводится дополнительная проверка на количество средств на карте.
                В случае если во время совершения транзакций кто-либо еще спишет с этой карты сумму, после которой
                остаток на карте не будет достаточен для проведения транзакции, то выполнение транзакций прервется,
                а предыдущие транзации не откатятся.**

            :param delay: Значение задержки между запросами, указывается в секундах.
            :type delay: float

            :param transactions: Список параметров транзакций
            :type transactions: List[Transaction]

            :raises SpwInsufficientFunds: Недостаточно средств на карте.
            :raises SpwCardNotFound: Карта получателя не найдена.
        """

        # Additional balance verify
        if self.get_balance() < sum([tr.amount for tr in transactions]):
            raise err.SpwInsufficientFunds()

        self._many_req(transactions, self.send_transaction, delay)
