import validators
from pydantic import BaseModel, field_validator

from .. import errors as err


class Payment(BaseModel):
    """
    Класс параметров оплаты.

    :param amount: Сумма которую должен оплатить пользователь.
    :type amount: int

    :param redirectUrl: Ссылка на которую перенаправит пользователя после успешной оплаты.
    :type redirectUrl: str

    :param webhookUrl: Ссылка вебхука, туда придет сообщение о успешной оплате.
    :type webhookUrl: str

    :param data: Полезные данные, которые вы хотите получить в будущем вместе с вебхуком.
    :type data: str

    :raises BigAmountError: Запрашиваемая сумма слишком большая *(макс. 1728)*
    :raises LengthError: Строка data слишком длинная *(макс. 100)*
    :raises IsNotURLError: Параметр не является URL
    """

    amount: int
    redirectUrl: str
    webhookUrl: str
    data: str

    @field_validator('amount')
    def _max_amount(cls, value: int):
        if value > 1728:
            raise err.BigAmountError()
        return value

    @field_validator('data')
    def _data_size(cls, value):
        if len(value) > 100:
            raise err.LengthError(100)
        return value

    @field_validator('redirectUrl', 'webhookUrl')
    def _verify_url(cls, value: str):
        if validators.url(value):
            return value
        raise err.IsNotURLError()


class Transaction(BaseModel):
    """
    Класс параметров транзакции.

    :param receiver: Карта получателя транзакции.
    :type receiver: str

    :param amount: Сумма которую должен оплатить пользователь.
    :type amount: int

    :param comment: Комментарий к транзакции.
    :type comment: str

    :raises LengthError: Комментарий к транзакции comment слишком длинный *(макс. 32)*
    :raises IsNotCardError: Неверно указана карта получателя
    """

    receiver: str
    amount: int
    comment: str

    @field_validator('comment')
    def _comment_size(cls, value: str):
        if len(value) > 32:
            raise err.LengthError(32)
        return value

    @field_validator('receiver')
    def _receiver_type(cls, value: str):
        if len(value) != 5 or not value.isnumeric():
            raise err.IsNotCardError(value)
        return value
