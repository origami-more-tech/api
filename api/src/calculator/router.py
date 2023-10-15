import json
from fastapi import APIRouter
from contstants import Collection
from calculator.model import Calc, CalcDTO
from office.model import Office
from datetime import datetime, timedelta
from utils.helpers import rank


router = APIRouter()
router.tags = [Collection.calc]


@router.post("/")
async def calculations_credit(calcDTO: CalcDTO) -> Calc:
    calcDTO.interest_rate /= 100
    # Расчет месячной процентной ставки
    monthly_interest_rate = calcDTO.interest_rate / 12
    # Расчет количества платежей
    num_payments = calcDTO.loan_term * 12
    # Расчет ежемесячного платежа
    monthly_payment = (calcDTO.loan_amount * monthly_interest_rate) / (
        1 - (1 + monthly_interest_rate) ** -num_payments
    )
    # Расчет итоговой переплаты
    sumFinaly = (monthly_payment * 12) * calcDTO.loan_term
    # Расчет переплаты по кредиту за указанный срок
    overPayment = sumFinaly - calcDTO.loan_amount
    dateLastPayment = (
        datetime.now() + timedelta(days=(calcDTO.loan_term * 365))
    ).strftime("%d.%m.%Y")

    with open("offices.json", encoding="utf-8") as json_file:
        offices = json.load(json_file)
        offices = rank(offices)
        office = Office(**offices[0])

    return Calc(
        monthlyPayment=round(monthly_payment, 2),
        sumCreditFull=round(sumFinaly, 2),
        sumPayment=round(monthly_payment, 2),
        overpayment=round(overPayment, 2),
        dateAtLast=dateLastPayment,
        office=office,
    )
