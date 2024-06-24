import uvicorn
import os
from contextlib import asynccontextmanager, closing
import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mbb.app.router import router as app_router
from mbb.moex.router import router as moex_router
from mbb.moex.service import search_all
from mbb.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    with closing(sqlite3.connect(settings.db_name, check_same_thread=False)) as connection:
        create_db(connection)
        # populate_db(connection)
        pass
    yield
    pass


application = FastAPI(lifespan=lifespan)

application.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

application.include_router(app_router, prefix="/app")
application.include_router(moex_router, prefix="/moex")


def start():
    uvicorn.run("mbb.main:application", host=settings.host, port=settings.port, reload=True)


def create_db(connection: sqlite3.Connection):
    ddl_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ddl.sql")
    with open(ddl_filename, "r") as file:
        sql = file.read()
    with closing(connection.cursor()) as cursor:
        cursor.executescript(sql)


def populate_db(connection: sqlite3.Connection):
    securities = search_all()
    sql = "INSERT OR IGNORE INTO Security VALUES " \
          "(:secid, :isin, :gosreg, :emitent_inn, :emitent_title, :type, :name, :shortname, :marketprice_boardid)"
    with closing(connection.cursor()) as cursor:
        cursor.executemany(sql, [x.model_dump() for x in securities if x is not None])
        connection.commit()
