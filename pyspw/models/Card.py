from typing import Optional

from pydantic import BaseModel


class SelfCard(BaseModel):
    balance: int
    webhook: str


class Card(BaseModel):
    id: Optional[str]
    name: str
    number: str
    color: Optional[str]
