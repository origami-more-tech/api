from fastapi import APIRouter
from contstants import Collection
from calculator.model import Calc
from datetime import datetime, timedelta


router = APIRouter()
router.tags = [Collection.calc]


@router.get("/")
async def calculations_credit(loan_amount: int, interest_rate: float, loan_term: int) -> Calc:
    interest_rate /= 100
    # Расчет месячной процентной ставки
    monthly_interest_rate = interest_rate / 12
    # Расчет количества платежей
    num_payments = loan_term * 12
    # Расчет ежемесячного платежа
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_payments)
    # Расчет итоговой переплаты
    sumFinaly = (monthly_payment * 12) * loan_term
    # Расчет переплаты по кредиту за указанный срок
    overPayment = sumFinaly - loan_amount
    dateLastPayment = (datetime.now() + timedelta(days=(loan_term * 365))).strftime("%d/%m/%Y")
    
    return Calc(sumCreditFull = sumFinaly, sumPayment = monthly_payment, overpayment=overPayment, dateAtLast=dateLastPayment)
