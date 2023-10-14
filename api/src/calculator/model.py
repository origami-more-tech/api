from pydantic import BaseModel, Field
from datetime import datetime


class Calc(BaseModel):
    sumCreditFull: float
    sumPayment: float
    overpayment: float
    createdAt: str = Field(default=datetime.now().strftime("%d/%m/%Y"))
    dateAtLast: str = Field(default=datetime.now().strftime("%d/%m/%Y"))
