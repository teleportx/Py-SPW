from pydantic import BaseModel


class SelfCard(BaseModel):
    balance: int
    webhook: str


class Card(BaseModel):
    name: str
    number: str
