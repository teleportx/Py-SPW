from typing import Optional, List

import validators
from pydantic import BaseModel, field_validator, Field

from .. import errors as err


class PaymentItem(BaseModel):
    name: str = Field(min_length=3, max_length=64)
    count: int = Field(ge=0, le=9999)
    price: int = Field(ge=1, le=1728)
    comment: Optional[str] = Field(min_length=3, max_length=64)


class Payment(BaseModel):
    """
    Класс параметров оплаты.

    :param redirectUrl: Ссылка на которую перенаправит пользователя после успешной оплаты.
    :type redirectUrl: str

    :param webhookUrl: Ссылка вебхука, туда придет сообщение о успешной оплате.
    :type webhookUrl: str

    :param data: Полезные данные, которые вы хотите получить в будущем вместе с вебхуком.
    :type data: str

    :raises IsNotURLError: Параметр не является URL
    """

    items: List[PaymentItem] = Field(min_length=1)
    redirectUrl: str
    webhookUrl: str
    data: str = Field(max_length=100)

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

    :raises IsNotCardError: Неверно указана карта получателя
    """

    receiver: str
    amount: int
    comment: str = Field(max_length=32)

    @field_validator('receiver')
    def _receiver_type(cls, value: str):
        if len(value) != 5 or not value.isnumeric():
            raise err.IsNotCardError(value)
        return value
