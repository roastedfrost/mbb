from fastapi import APIRouter
from mbb.moex.service import fetch_securities, fetch_marketdata, search_all

router = APIRouter()


@router.get('/securities')
def fetch_securities_route():
    return fetch_securities()


@router.get('/marketdata')
def fetch_marketdata_route():
    return fetch_marketdata()


@router.get('/search')
def search_route():
    return search_all()
