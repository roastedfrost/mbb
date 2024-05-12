from typing_extensions import List
from scipy.optimize import anderson, newton
from mbb.math.models import PaymentItem


def compute_full_price(facevalue: float, value: float, accrued_int: float):
    return facevalue * value / 100 + accrued_int


def xnpv(rate: float, payments: List[PaymentItem]):
    if rate <= -1.0:
        return float('inf')
    closest_payment = min(payments, key=lambda x: x.date)
    return sum([
        x.value / (1 + rate) ** ((x.date - closest_payment.date).days / 365)
        for x in payments
    ])


class CalcMethod(str, Enum):
    NEWTON = 'newton'
    ANDERSON = 'anderson'


def xirr(payments: List[PaymentItem], method: CalcMethod = CalcMethod.ANDERSON):
    if method == CalcMethod.NEWTON:
        return newton(lambda r: xnpv(r, payments), 0)
    if method == CalcMethod.ANDERSON:
        return anderson(lambda r: xnpv(r, payments), 0)
    raise BaseException()


def compute_xirr(expenses: List[PaymentItem], income: List[PaymentItem], method: CalcMethod = CalcMethod.ANDERSON):
    payments = [PaymentItem(value=x.value * -1, date=x.date) for x in income] + expenses
    rate = xirr(payments=payments, method=method)
    return rate
