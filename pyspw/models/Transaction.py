from typing import List, Any

import validators
from pydantic import BaseModel, field_validator, Field


class PaymentItem(BaseModel):
    """**Товар для оплаты**"""

    """Название товара"""
    name: str = Field(min_length=3, max_length=64)
    """Количество товара."""
    count: int = Field(ge=1, le=9999)
    """Цена товара."""
    price: int = Field(ge=1, le=1728)
    """Комментарий к товару."""
    comment: str = Field(min_length=3, max_length=64, default=None)


class Payment(BaseModel):
    """**Параметры оплаты**"""

    items: List[PaymentItem] = Field(min_length=1)
    """Список товаров, которые оплачивает пользователь"""
    redirectUrl: str
    """Ссылка на которую перенаправит пользователя после успешной оплаты"""
    webhookUrl: str
    """Ссылка вебхука, туда придет сообщение об успешной оплат."""
    data: str = Field(max_length=100)
    """Полезные данные, которые вы хотите получить в будущем вместе с вебхуком"""

    @field_validator('redirectUrl', 'webhookUrl')
    def verify_url(cls, value: str):
        """Проверяет URL на валидность"""

        if validators.url(value):
            return value
        raise ValueError('Field is not url.')

    @field_validator('items')
    def verify_amount(cls, value: List[PaymentItem]) -> List[PaymentItem]:
        """Проверяет не превышен ли придел в 10000 на общую сумму товаров"""

        amount = 0
        for el in value:
            amount += el.count * el.price

        if amount > 10000:
            raise ValueError('Maximal summary amount may be not greater than 10000')

        return value

    def model_dump(self, *args, **kwargs) -> Any:
        """:meta private:"""

        kwargs['exclude_defaults'] = True
        return super().model_dump(*args, **kwargs)


class Transaction(BaseModel):
    """**Параметры транзакции**"""

    receiver: str
    """Карта получателя тразакции"""
    amount: int = Field(ge=1)
    """Сумма которую должен оплатить пользователь"""
    comment: str = Field(min_length=1, max_length=32)
    """Комментарий к транзакции"""

    @field_validator('receiver')
    def receiver_type(cls, value: str):
        """Проверяет номер карты на валидность"""

        if len(value) != 5 or not value.isnumeric():
            raise ValueError(f'Receiver card (`{value}`) number not valid')
        return value
