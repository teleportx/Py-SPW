from pydantic import BaseModel, validator
import validators


class Payment(BaseModel):
    amount: int
    redirectUrl: str
    webhookUrl: str
    data: str

    @validator('amount')
    def max_amount(cls, value: int):
        if value > 1728:
            raise ValueError('amount must be <= 1728')
        return value

    @validator('data')
    def data_size(cls, value):
        if len(value) > 100:
            raise ValueError('data length must be <=100.')
        return value

    @validator('redirectUrl', 'webhookUrl')
    def verify_url(cls, value: str):
        if validators.url(value):
            return value
        raise ValueError('is not url')


class Transaction(BaseModel):
    receiver: str
    amount: int
    comment: str

    @validator('comment')
    def comment_size(cls, value: str):
        if len(value) > 32:
            raise ValueError('comment length must be <=32.')
        return value

    @validator('receiver')
    def receiver_type(cls, value: str):
        if len(value) != 5 or not value.isnumeric():
            raise ValueError(f'Receiver card (`{value}`) number not valid')
        return value
