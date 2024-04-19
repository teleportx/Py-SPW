from ..methods.base import BaseMethod, RequestTypes
from ..models.ServerAnswers import CreatePaymentAnswer
from ..models import Payment


class CreatePayment(BaseMethod[CreatePaymentAnswer]):
    """
    Создает ссылку на оплату для пользователя.

    https://github.com/sp-worlds/api-docs/wiki/%D0%9E%D0%BF%D0%BB%D0%B0%D1%82%D0%B0-%D0%BD%D0%B0-%D0%B2%D0%B0%D1%88%D0%B5%D0%BC-%D1%81%D0%B0%D0%B9%D1%82%D0%B5
    """

    __returns__ = CreatePaymentAnswer
    __method__ = '/payments'
    __request_type__ = RequestTypes.POST

    def __init__(self, payment: Payment):
        super().__init__(**payment.model_dump())
