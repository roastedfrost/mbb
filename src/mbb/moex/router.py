from fastapi import APIRouter
from mbb.moex.service import fetch_securities

router = APIRouter()


@router.get('/securities')
def fetch_securities_route():
    return fetch_securities()
