import sqlite3
from typing import Annotated
from fastapi import APIRouter, Depends
from mbb.dependencies import get_db_conn
from mbb.app.service import search_all

router = APIRouter()


@router.get('/search')
def search_route(connection: Annotated[sqlite3.Connection, Depends(dependency=get_db_conn)]):
    return search_all(connection=connection)