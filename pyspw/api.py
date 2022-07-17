from base64 import b64encode
from hashlib import sha256
import hmac
import requests as rq
import time

from . import errors as err

accessed_body_part = ['face', 'front', 'frontfull', 'head', 'bust', 'full', 'skin']


class sp_api_base:
    def __init__(self, card_id: str, card_token: str):
        self.card_token = card_token
        self.authorization = f"Bearer {str(b64encode(str(f'{card_id}:{card_token}').encode('utf-8')), 'utf-8')}"
        self.host = 'https://spworlds.ru/api/public'

    def __str__(self):
        pass

    def __get(self, path: str = None, ignore_status_code: bool = False) -> rq.Response:
        headers = {
            'Authorization': self.authorization,
            'User-Agent': 'Py-SPW'
        }
        try:
            response = rq.get(url=self.host + path, headers=headers)

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
            'Authorization': self.authorization,
            'User-Agent': 'Py-SPW'
        }
        try:
            response = rq.post(url=self.host + path, headers=headers, json=body)

        except rq.exceptions.ConnectionError as error:
            raise err.SpwApiError(error)

        if response.status_code == 200:
            return response

        elif response.status_code >= 500:
            raise err.SpwApiError(f'HTTP: {response.status_code}, Server Error.')

        else:
            raise err.SpwApiError(f'HTTP: {response.status_code} {response.json()["error"]}. Message: {response.json()["message"]}')

    def get_user(self, discord_id: str) -> str | None:
        """
            Получение ника пользователя.
            :param discord_id: ID пользователя дискорда.
            :return: Str если пользователь найден, None если пользователь не найден. В str содержиться никнейм пользователя
        """
        response = self.__get(f'/users/{discord_id}', True)

        if response.status_code == 200:
            return response.json()['username']

        elif response.status_code == 404:
            return None

        elif response.status_code >= 500:
            raise err.SpwApiError(f'HTTP: {response.status_code}, Server Error.')

        else:
            raise err.SpwApiError(f'HTTP: {response.status_code} {response.json()["error"]}. Message: {response.json()["message"]}')

    def check_access(self, discord_id: str) -> bool:
        """
            Получение статуса проходки.
            :param discord_id: ID пользователя дискорда.
            :return: Bool - False если у пользователя не имеется проходки, True если у пользователя есть проходка
        """
        return False if self.get_user(discord_id) is None else True

    def get_user_skin_url(self, discord_id: str, body_part: str, image_size: int = 64) -> str | None:
        """
            Получение изображения части скина.
            :param discord_id: ID пользователя дискорда.
            :param body_part: Часть тела для получения. Допустимые значения - https://visage.surgeplay.com/index.html
            :param image_size: Размер получаемого изображения.
            :return: Str если пользователь найден, None если пользователь не найден. В str содержится ссылка на изображение профиля
        """

        if body_part not in accessed_body_part:
            raise err.BadSkinPartName(f'"{body_part}" is not a part of the skin')

        username = self.get_user(discord_id)
        if username is not None:
            # mojang
            try:
                mojang_response = rq.get(f'https://api.mojang.com/users/profiles/minecraft/{username}')
                if mojang_response.status_code != 200:
                    raise err.MojangApiError(f'HTTP status: {mojang_response.status_code}')
                uuid = mojang_response.json()['id']

            except rq.exceptions.ConnectionError as error:
                raise err.MojangApiError(error)

            except rq.exceptions.JSONDecodeError:
                return None

            # surgeplay
            return f'https://visage.surgeplay.com/{body_part}/{image_size}/{uuid}'

        else:
            return None

    def get_user_skin(self, discord_id: str, body_part: str, image_size: int = 64) -> bytes | None:
        """
            Получение изображения части скина.
            :param discord_id: ID пользователя дискорда.
            :param body_part: Часть тела для получения. Допустимые значения - https://visage.surgeplay.com/index.html
            :param image_size: Размер получаемого изображения.
            :return: Bytes если пользователь найден, None если пользователь не найден. В bytes содержиться изображение профиля
        """
        url = self.get_user_skin_url(discord_id, body_part, image_size)
        if url is None:
            return None

        try:
            surgeplay_response = rq.get(url)
            if surgeplay_response.status_code != 200:
                raise err.SurgeplayApiError(f'HTTP status: {surgeplay_response.status_code}')
            return surgeplay_response.content

        except rq.exceptions.ConnectionError as error:
            raise err.SurgeplayApiError(error)

    def check_webhook(self, webhook_data: str, X_Body_Hash: str) -> bool:
        """
            Валидирует webhook
            :param webhook_data: Тело webhook'а.
            :param X_Body_Hash: Хэдер X-Body-Hash из webhook.
            :return: Bool True если вебхук пришел от верифицированного сервера, иначе False
        """
        hmac_data = hmac.new(self.card_token.encode('utf-8'), webhook_data.encode('utf-8'), sha256).digest()
        base64_data = b64encode(hmac_data)
        return hmac.compare_digest(base64_data, X_Body_Hash.encode('utf-8'))

    def create_payment(self, amount: int, redirectUrl: str, webhookUrl: str, data: str = '') -> str:
        """
            Создание ссылки на оплату
            :param amount: Стоимость покупки в АРах.
            :param redirectUrl: URL страницы, на которую попадет пользователь после оплаты.
            :param webhookUrl: URL, куда наш сервер направит запрос, чтобы оповестить ваш сервер об успешной оплате.
            :param data: Строка до 100 символов, сюда можно пометить любые полезные данных.
            :return: Str ссылка на страницу оплаты, на которую стоит перенаправить пользователя.
        """
        body = {
            'amount': amount,
            'redirectUrl': redirectUrl,
            'webhookUrl': webhookUrl,
            'data': data
        }
        return self.__post('/payment', body).json()['url']

    def create_payments(self, payments: tuple, request_delay: float = 0.1) -> list:
        """
            Создание ссылок на оплату
            :param request_delay: Значение задержки между запросами, указывается в секундах
            :param payments: Кортеж содержащий словари со следующими параметрами:
                :parameter amount: Стоимость покупки в АРах.
                :parameter redirectUrl: URL страницы, на которую попадет пользователь после оплаты.
                :parameter webhookUrl: URL, куда наш сервер направит запрос, чтобы оповестить ваш сервер об успешной оплате.
                :parameter data: Строка до 100 символов, сюда можно пометить любые полезные данных.
            :return: List с ссылками на страницы оплаты, в том порядке, в котором они были в кортеже payments
        """
        answer = []
        for payment in payments:
            try:
                answer.append(self.create_payment(
                    int(payment['amount']),
                    str(payment['redirectUrl']),
                    str(payment['webhookUrl']),
                    str(payment['data'])
                ))

            except ValueError:
                raise err.BadParameter('Amount must be int')

            except KeyError as error:
                raise err.BadParameter(f'Missing parameter {error}')

            time.sleep(request_delay)

        return answer

    def send_transaction(self, receiver: str, amount: int, comment: str = 'Нет комментария') -> None:
        """
            Отправка транзакции
            :param receiver: Номер карты на которую будет совершена транзакция.
            :param amount: Сумма транзакции.
            :param comment: Комментарий к транзакции.
            :return: None.
        """
        body = {
            'receiver': receiver,
            'amount': amount,
            'comment': comment
        }
        self.__post('/transactions', body)

    def send_transactions(self, transactions: tuple, request_delay: float = 0.1) -> None:
        """
            Отправка транзакций
            :param request_delay: Значение задержки между запросами, указывается в секундах
            :param transactions: Кортеж содержащий словари со следующими параметрами:
                :param receiver: Номер карты на которую будет совершена транзакция.
                :param amount: Сумма транзакции.
                :param comment: Комментарий к транзакции.
            :return: List с ссылками на страницы оплаты, в том порядке, в котором они были в кортеже payments
        """
        for transaction in transactions:
            try:
                self.send_transaction(
                    str(transaction['receiver']),
                    int(transaction['amount']),
                    str(transaction['comment'])
                )

            except ValueError:
                raise err.BadParameter('Amount must be int')

            except KeyError as error:
                raise err.BadParameter(f'Missing parameter {error}')

            time.sleep(request_delay)

    def get_balance(self) -> int:
        return self.__get('/card').json()['balance']
