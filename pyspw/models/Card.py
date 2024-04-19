from typing import Optional

from pydantic import BaseModel


class SelfCard(BaseModel):
    balance: int
    webhook: Optional[str]


class Card(BaseModel):
    id: Optional[str] = None
    name: str
    number: str
    color: Optional[int] = None
