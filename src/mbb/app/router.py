import sqlite3
from typing_extensions import Annotated, List
from fastapi import APIRouter, Depends
from mbb.dependencies import get_db_conn
from mbb.moex.models import SecuritySearchItem
from mbb.app.service import search_all, get_bookmarks
from mbb.app.models import BookmarkItem

router = APIRouter()


@router.get('/search', response_model=List[SecuritySearchItem])
def search_route(connection: Annotated[sqlite3.Connection, Depends(dependency=get_db_conn)]):
    return search_all(connection=connection)


@router.get('/bookmarks', response_model=List[BookmarkItem])
def get_bookmarks_route(connection: Annotated[sqlite3.Connection, Depends(dependency=get_db_conn)]):
    return get_bookmarks(connection=connection)
