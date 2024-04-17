from pydantic import BaseModel


class CreatePaymentAnswer(BaseModel):
    url: str
