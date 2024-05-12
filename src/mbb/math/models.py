from datetime import datetime
from pydantic import BaseModel


class PaymentItem(BaseModel):
    value: float
    date: datetime