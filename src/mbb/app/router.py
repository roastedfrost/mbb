import sqlite3
from typing_extensions import Annotated, List
from fastapi import APIRouter, Depends
from mbb.dependencies import get_db_conn
from mbb.moex.models import SecuritySearchItem, SecurityItem
from mbb.app.service import search_all, get_bookmarks, fetch_securities
from mbb.app.models import BookmarkItem

router = APIRouter()


@router.get('/search', response_model=List[SecuritySearchItem])
def search_all_route(connection: Annotated[sqlite3.Connection, Depends(dependency=get_db_conn)]):
    return search_all(connection=connection)


@router.get('/securities', response_model=List[SecurityItem])
def fetch_securities_route(connection: Annotated[sqlite3.Connection, Depends(dependency=get_db_conn)]):
    return fetch_securities(connection=connection)


@router.get('/bookmarks', response_model=List[BookmarkItem])
def get_bookmarks_route(connection: Annotated[sqlite3.Connection, Depends(dependency=get_db_conn)]):
    return get_bookmarks(connection=connection)
