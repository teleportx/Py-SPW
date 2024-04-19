from ..methods.base import BaseMethod, RequestTypes
from ..models.ServerAnswers import CreateTransactionAnswer
from ..models import Transaction


class CreateTransaction(BaseMethod[CreateTransactionAnswer]):
    """
    Отправляет транзакцию.

    https://github.com/sp-worlds/api-docs/wiki/%D0%91%D0%B0%D0%BD%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B5-%D0%BF%D0%B5%D1%80%D0%B5%D0%B2%D0%BE%D0%B4%D1%8B
    """

    __returns__ = CreateTransactionAnswer
    __method__ = '/transactions'
    __request_type__ = RequestTypes.POST

    def __init__(self, transaction: Transaction):
        super().__init__(**transaction.model_dump())
