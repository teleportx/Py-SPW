from pydantic import BaseModel


class CreatePaymentAnswer(BaseModel):
    url: str


class CreateTransactionAnswer(BaseModel):
    balance: int


class SetTransactionWebhookAnswer(BaseModel):
    id: str
    webhook: str
