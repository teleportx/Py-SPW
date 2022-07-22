from base64 import b64encode
from hashlib import sha256
import hmac
import requests as rq
import time
from typing import Optional, List
import logging
from mojang import MojangAPI

from . import errors as err
from .User import User
from .Parameters import PaymentParameters, TransactionParameters

# deesiigneer stole some of my ideas and improved them. But I didn't lose my head and improved what deesiigneer improved :)


class Py_SPW:
    __spworlds_api_url = 'https://spworlds.ru/api/public'

    def __init__(self, card_id: str, card_token: str):
        self.__card_token = card_token
        self.__authorization = f"Bearer {str(b64encode(str(f'{card_id}:{card_token}').encode('utf-8')), 'utf-8')}"

    def __get(self, path: str = None, ignore_status_code: bool = False) -> rq.Response:
        headers = {
            'Authorization': self.__authorization,
            'User-Agent': 'Py-SPW'
        }
        try:
            response = rq.get(url=self.__spworlds_api_url + path, headers=headers)

        except rq.exceptions.ConnectionError as error:
            raise err.SpwApiError(error)

        if ignore_status_code:
            return response

        if response.status_code == 200:
            return response

        elif response.status_code >= 500:
            raise err.SpwApiError(f'HTTP: {response.status_code}, Server Error.')

        else:
            raise err.SpwApiError(
                f'HTTP: {response.status_code} {response.json()["error"]}. Message: {response.json()["message"]}')

    def __post(self, path: str = None, body: dict = None) -> rq.Response:
        headers = {
            'Authorization': self.__authorization,
            'User-Agent': 'Py-SPW'
        }
        try:
            response = rq.post(url=self.__spworlds_api_url + path, headers=headers, json=body)

        except rq.exceptions.ConnectionError as error:
            raise err.SpwApiError(error)

        if response.status_code == 200:
            return response

        elif response.status_code >= 500:
            raise err.SpwApiError(f'HTTP: {response.status_code}, Server Error.')

        else:
            raise err.SpwApiError(f'HTTP: {response.status_code} {response.json()["error"]}. Message: {response.json()["message"]}')

    def get_user(self, discord_id: str, use_mojang_api: bool = True) -> User:
        """
            Получение пользователя
            :param use_mojang_api: Если True то будет обращаться к Mojang API для получения UUID, иначе обращаться не будет
            :param discord_id: ID пользователя дискорда.
            :return: Class pyspw.User.User
        """

        response = self.__get(f'/users/{discord_id}', True)

        if response.status_code == 200:
            return User(response.json()['username'], use_mojang_api)

        elif response.status_code == 404:
            return User(None, use_mojang_api)

        elif response.status_code >= 500:
            raise err.SpwApiError(f'HTTP: {response.status_code}, Server Error.')

        else:
            raise err.SpwApiError(f'HTTP: {response.status_code} {response.json()["error"]}. Message: {response.json()["message"]}')

    def get_users(self, discord_ids: List[str], delay: float = 0.5, use_mojang_api: bool = True) -> List[User]:
        """
            Получение пользователей
            :param use_mojang_api: Если True то будет обращаться к Mojang API для получения UUID, иначе обращаться не будет
            :param delay: Значение задержки между запросами, указывается в секундах
            :param discord_ids: List с IDs пользователей дискорда.
            :return: List содержащий Classes pyspw.User.User
        """

        users = []

        if len(discord_ids) > 100 and delay < 0.5:
            logging.warning('You send DOS attack to SPWorlds API. Please set the delay to greater than or equal to 0.5')

        for discord_id in discord_ids:
            users.append(self.get_user(discord_id, False))
            time.sleep(delay)

        if use_mojang_api:
            nicknames = [user.nickname for user in users]
            uuids = MojangAPI.get_uuids(nicknames)

            for user in users:
                user.uuid = uuids[user.nickname]

        return users

    def check_access(self, discord_id: str) -> bool:
        """
            Получение статуса проходки
            :param discord_id: ID пользователя дискорда.
            :return: Bool True если у пользователя есть проходка, иначе False
        """
        return self.get_user(discord_id, False).access

    def check_accesses(self, discord_ids: List[str], delay: float = 0.5) -> List[bool]:
        """
            Получение статуса проходок
            :param delay: Значение задержки между запросами, указывается в секундах
            :param discord_ids: List с IDs пользователей дискорда.
            :return: List содержащий bool со значением статуса проходки
        """

        accesses = []

        users = self.get_users(discord_ids, delay, False)

        if len(discord_ids) > 100 and delay < 0.5:
            logging.warning('You send DOS attack to SPWorlds API. Please set the delay to greater than or equal to 0.5')

        for user in users:
            if user is not None:
                accesses.append(True)

            else:
                accesses.append(False)

        return accesses

    def check_webhook(self, webhook_data: str, X_Body_Hash: str) -> bool:
        """
            Валидирует webhook
            :param webhook_data: Тело webhook'а.
            :param X_Body_Hash: Хэдер X-Body-Hash из webhook.
            :return: Bool True если вебхук пришел от верифицированного сервера, иначе False
        """

        hmac_data = hmac.new(self.__card_token.encode('utf-8'), webhook_data.encode('utf-8'), sha256).digest()
        base64_data = b64encode(hmac_data)
        return hmac.compare_digest(base64_data, X_Body_Hash.encode('utf-8'))

    def create_payment(self, params: PaymentParameters) -> str:
        """
            Создание ссылки на оплату
            :param params: class PaymentParams параметров оплаты
            :return: Str ссылка на страницу оплаты, на которую стоит перенаправить пользователя.
        """

        body = {
            'amount': params.amount,
            'redirectUrl': params.redirectUrl,
            'webhookUrl': params.webhookUrl,
            'data': params.data
        }
        return self.__post('/payment', body).json()['url']

    def create_payments(self, payments: List[PaymentParameters], delay: float = 0.5) -> list:
        """
            Создание ссылок на оплату
            :param payments: Список содержащий classes PaymentParams
            :param delay: Значение задержки между запросами, указывается в секундах
            :return: List со ссылками на страницы оплаты, в том порядке, в котором они были в кортеже payments
        """

        answer = []

        if len(payments) > 100 and delay < 0.5:
            logging.warning('You send DOS attack to SPWorlds API. Please set the delay to greater than or equal to 0.5')

        for payment in payments:
            answer.append(self.create_payment(payment))
            time.sleep(delay)

        return answer

    def send_transaction(self, params: TransactionParameters) -> None:
        """
            Отправка транзакции
            :param params: class TransactionParameters параметры транзакции
            :return: None.
        """

        body = {
            'receiver': params.receiver,
            'amount': params.amount,
            'comment': params.comment
        }
        self.__post('/transactions', body)

    def send_transactions(self, transactions: List[TransactionParameters], delay: float = 0.1) -> None:
        """
            Отправка транзакций
            :param delay: Значение задержки между запросами, указывается в секундах
            :param transactions: Список содержащий classes TransactionParameters
            :return: List со ссылками на страницы оплаты, в том порядке, в котором они были в кортеже payments
        """

        if len(transactions) > 100 and delay < 0.5:
            logging.warning('You send DOS attack to SPWorlds API. Please set the delay to greater than or equal to 0.5')

        for transaction in transactions:
            self.send_transaction(transaction)
            time.sleep(delay)

    def get_balance(self) -> int:
        """
            Получение баланса
            :return: Int со значением баланса
        """

        return self.__get('/card').json()['balance']
