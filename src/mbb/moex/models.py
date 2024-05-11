from typing_extensions import Optional
from datetime import datetime
from pydantic import BaseModel, field_validator


class SecurityItem(BaseModel):
    secid: str
    isin: str
    issuesize: int
    issuesizeplaced: Optional[int]
    settledate: datetime
    couponpercent: Optional[float]
    couponvalue: float
    nextcoupon: Optional[datetime]
    couponperiod: int
    accruedint: float
    facevalue: float
    facevalueonsettledate: Optional[float]
    matdate: Optional[datetime]
    offerdate: Optional[datetime]
    buybackprice: Optional[float]
    buybackdate: Optional[datetime]

    @field_validator("settledate", "nextcoupon", "matdate", "offerdate", "buybackdate", mode="before")
    @staticmethod
    def convert_to_datetime(date_str: str):
        return str_to_date(date_str)


class SecurityMarketDataItem(BaseModel):
    secid: str
    last: Optional[float]
    yield_: Optional[float]


class SecuritySearchItem(BaseModel):
    secid: str
    isin: str
    gosreg: Optional[str]
    emitent_inn: str
    emitent_title: str
    type: str
    name: str
    shortname: str
    marketprice_boardid: Optional[str]


def str_to_date(x: str):
    if x == "0000-00-00":
        return None
    return x and datetime.strptime(x, "%Y-%m-%d").date()
