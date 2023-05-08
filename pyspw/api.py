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
from .User import User
from .Parameters import Payment, Transaction

mapi = MAPI()


class _RequestTypes(Enum):
    POST = 'POST'
    GET = 'GET'


@dataclass
class _Card:
    id: str
    token: str


class SpApi:
    _spworlds_api_url = 'https://spworlds.ru/api/public'

    def __init__(self, card_id: str, card_token: str):
        self._card = _Card(card_id, card_token)
        self._authorization = f"Bearer {str(b64encode(str(f'{card_id}:{card_token}').encode('utf-8')), 'utf-8')}"

    def _request(self, method: _RequestTypes, path: str = '', body: dict = None, *,
                 ignore_codes: list = []) -> rq.Response:
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
            Проверка работоспособности API
            :return: Bool работает или нет
        """
        try:
            self.get_balance()
            return True

        except err.SpwApiError:
            return False

    def get_user(self, discord_id: str) -> User:
        """
            Получение пользователя
            :param discord_id: ID пользователя дискорда.
            :return: Class pyspw.User.User
        """

        response = self._request(_RequestTypes.GET, f'/users/{discord_id}', ignore_codes=[404])
        if response.status_code == 404:
            raise err.SpwUserNotFound(discord_id)

        return User(response.json()['username'])

    def check_access(self, discord_id: str) -> bool:
        """
            Получение статуса проходки
            :param discord_id: ID пользователя дискорда.
            :return: Bool True если у пользователя есть проходка, иначе False
        """
        response = self._request(_RequestTypes.GET, f'/users/{discord_id}', ignore_codes=[404])
        return response.status_code != 404

    def check_webhook(self, webhook_data: str, X_Body_Hash: str) -> bool:
        """
            Валидирует webhook
            :param webhook_data: Тело webhook'а.
            :param X_Body_Hash: Хэдер X-Body-Hash из webhook.
            :return: Bool True если вебхук пришел от верифицированного сервера, иначе False
        """

        hmac_data = hmac.new(self._card.token.encode('utf-8'), webhook_data.encode('utf-8'), sha256).digest()
        base64_data = b64encode(hmac_data)
        return hmac.compare_digest(base64_data, X_Body_Hash.encode('utf-8'))

    def create_payment(self, params: Payment) -> str:
        """
            Создание ссылки на оплату
            :param params: class PaymentParams параметров оплаты
            :return: Str ссылка на страницу оплаты, на которую стоит перенаправить пользователя.
        """
        return self._request(_RequestTypes.POST, '/payment', params.dict()).json()['url']

    def send_transaction(self, params: Transaction) -> None:
        """
            Отправка транзакции
            :param params: class TransactionParameters параметры транзакции
            :return: None.
        """
        response = self._request(_RequestTypes.POST, '/transactions', params.dict(), ignore_codes=[400])
        if response.status_code == 400 and response.json()["message"] == 'Недостаточно средств на карте':
            raise err.SpwInsufficientFunds()

    def get_balance(self) -> int:
        """
            Получение баланса
            :return: Int со значением баланса
        """
        return self._request(_RequestTypes.GET, '/card').json()['balance']

    # Manys
    def _many_req(self, iterable: List, method: Callable, delay: float) -> List:
        users = []

        if len(iterable) > 100 and delay <= 0.5:
            logging.warning('You send DOS attack to SPWorlds API. Please set the delay to greater than to 0.5')

        for i in iterable:
            users.append(method(i))
            time.sleep(delay)

        return users

    def get_users(self, discord_ids: List[str], delay: float = 0.3) -> List[User]:
        """
            Получение пользователей
            :param delay: Значение задержки между запросами, указывается в секундах
            :param discord_ids: List с IDs пользователей дискорда.
            :return: List содержащий Classes pyspw.User.User
        """
        return self._many_req(discord_ids, self.get_user, delay)

    def check_accesses(self, discord_ids: List[str], delay: float = 0.3) -> List[bool]:
        """
            Получение статуса проходок
            :param delay: Значение задержки между запросами, указывается в секундах
            :param discord_ids: List с IDs пользователей дискорда.
            :return: List содержащий bool со значением статуса проходки
        """
        return self._many_req(discord_ids, self.check_access, delay)

    def create_payments(self, payments: List[Payment], delay: float = 0.5) -> List[str]:
        """
            Создание ссылок на оплату
            :param payments: Список содержащий classes PaymentParams
            :param delay: Значение задержки между запросами, указывается в секундах
            :return: List со ссылками на страницы оплаты, в том порядке, в котором они были в кортеже payments
        """
        return self._many_req(payments, self.create_payment, delay)

    def send_transactions(self, transactions: List[Transaction], delay: float = 0.5) -> None:
        """
            Отправка транзакций
            :param delay: Значение задержки между запросами, указывается в секундах
            :param transactions: Список содержащий classes TransactionParameters
            :return: List со ссылками на страницы оплаты, в том порядке, в котором они были в кортеже payments
        """
        self._many_req(transactions, self.send_transaction, delay)
