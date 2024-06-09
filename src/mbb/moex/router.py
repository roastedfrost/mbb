from typing_extensions import Union, List
from fastapi import APIRouter
from mbb.moex.models import SecurityItem, SecuritySearchItem, SecurityMarketDataItem
from mbb.moex.service import fetch_securities, fetch_marketdata, search_all

router = APIRouter()


@router.get('/securities', response_model=List[Union[SecurityItem, None]])
def fetch_securities_route():
    return fetch_securities()


@router.get('/marketdata', response_model=List[Union[SecurityMarketDataItem, None]])
def fetch_marketdata_route():
    return fetch_marketdata()


@router.get('/search', response_model=List[Union[SecuritySearchItem, None]])
def search_route():
    return search_all()
