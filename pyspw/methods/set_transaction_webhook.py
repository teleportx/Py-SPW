import validators

from pyspw import errors
from pyspw.methods.base import BaseMethod, RequestTypes
from pyspw.models import SetTransactionWebhookAnswer


class SetTransactionWebhook(BaseMethod[SetTransactionWebhookAnswer]):
    """
    Устанавливает ссылку для приема вебхуков о всех транзакциях, поступающих на карту.

    https://github.com/sp-worlds/api-docs/wiki/%D0%98%D0%B7%D0%BC%D0%B5%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5-%D0%B2%D0%B5%D0%B1%D1%85%D1%83%D0%BA%D0%B0-%D0%BA%D0%B0%D1%80%D1%82%D1%8B
    """

    __returns__ = SetTransactionWebhookAnswer
    __method__ = '/card/webhook'
    __request_type__ = RequestTypes.PUT

    def __init__(self, url: str):
        if not validators.url(url):
            raise errors.IsNotURLError()

        super().__init__(url=url)
