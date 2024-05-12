import sqlite3
from mbb.settings import settings
from contextlib import closing


def get_db_conn():
    with closing(sqlite3.connect(settings.db_name, check_same_thread=False)) as connection:
        connection.row_factory = sqlite3.Row
        yield connection
