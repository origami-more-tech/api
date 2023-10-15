from pydantic import BaseModel, Field
from datetime import datetime
from office.model import Office


class Calc(BaseModel):
    monthlyPayment: float
    sumCreditFull: float
    sumPayment: float
    overpayment: float
    createdAt: str = Field(default=datetime.now().strftime("%d.%m.%Y"))
    dateAtLast: str = Field(default=datetime.now().strftime("%d.%m.%Y"))
    office: Office


class CalcDTO(BaseModel):
    loan_amount: int
    interest_rate: float
    loan_term: int
