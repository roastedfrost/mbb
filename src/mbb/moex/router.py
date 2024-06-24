import sqlite3
from typing_extensions import Union, Annotated, List
from fastapi import APIRouter, Depends
from mbb.dependencies import get_db_conn
from mbb.moex.models import SecurityItem, SecuritySearchItem, SecurityMarketDataItem
from mbb.moex.service import fetch_securities, fetch_marketdata, search_all


router = APIRouter()


@router.get('/securities', response_model=List[Union[SecurityItem, None]])
def fetch_securities_route(connection: Annotated[sqlite3.Connection, Depends(dependency=get_db_conn)]):
    return fetch_securities(connection)


@router.get('/marketdata', response_model=List[Union[SecurityMarketDataItem, None]])
def fetch_marketdata_route():
    return fetch_marketdata()


@router.get('/search', response_model=List[Union[SecuritySearchItem, None]])
def search_all_route():
    return search_all()
