from typing import List, Any

import validators
from pydantic import BaseModel, field_validator, Field


class PaymentItem(BaseModel):
    """
    Класс параметров оплаты.

    :param name: Название товара
    :type name: str

    :param count: Количество товара.
    :type count: int

    :param price: Цена товара.
    :type price: int

    :param comment: Комментарий к товару. _(необяз.)_
    :type comment: str
    """

    name: str = Field(min_length=3, max_length=64)
    count: int = Field(ge=1, le=9999)
    price: int = Field(ge=1, le=1728)
    comment: str = Field(min_length=3, max_length=64, default=None)


class Payment(BaseModel):
    """
    Класс параметров оплаты.

    :param items: Список товаров, которые оплачивает пользователь.
    :type items: List[PaymentItem]

    :param redirectUrl: Ссылка на которую перенаправит пользователя после успешной оплаты.
    :type redirectUrl: str

    :param webhookUrl: Ссылка вебхука, туда придет сообщение об успешной оплате.
    :type webhookUrl: str

    :param data: Полезные данные, которые вы хотите получить в будущем вместе с вебхуком.
    :type data: str

    :raises ValidationError: webhookUrl не является URL.
    :raises ValidationError: redirectUrl не является URL.
    :raises ValidationError: Максимальная сумма превышает 10000.
    """

    items: List[PaymentItem] = Field(min_length=1)
    redirectUrl: str
    webhookUrl: str
    data: str = Field(max_length=100)

    @field_validator('redirectUrl', 'webhookUrl')
    def _verify_url(cls, value: str):
        if validators.url(value):
            return value
        raise ValueError('Field is not url.')

    @field_validator('items')
    def _verify_items(cls, value: List[PaymentItem]) -> List[PaymentItem]:
        amount = 0
        for el in value:
            amount += el.count * el.price

        if amount > 10000:
            raise ValueError('Maximal summary amount may be not greater than 10000')

        return value

    def model_dump(self, *args, **kwargs) -> Any:
        kwargs['exclude_defaults'] = True
        return super().model_dump(*args, **kwargs)


class Transaction(BaseModel):
    """
    Класс параметров транзакции.

    :param receiver: Карта получателя транзакции.
    :type receiver: str

    :param amount: Сумма которую должен оплатить пользователь.
    :type amount: int

    :param comment: Комментарий к транзакции.
    :type comment: str

    :raises ValidationError: Карта получателя имеет неверный формат.
    """

    receiver: str
    amount: int = Field(ge=1)
    comment: str = Field(min_length=1, max_length=32)

    @field_validator('receiver')
    def _receiver_type(cls, value: str):
        if len(value) != 5 or not value.isnumeric():
            raise ValueError(f'Receiver card (`{value}`) number not valid')
        return value
