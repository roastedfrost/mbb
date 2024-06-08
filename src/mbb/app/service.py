from contextlib import closing
import sqlite3
from mbb.moex.models import SecuritySearchItem


def search_all(connection: sqlite3.Connection):
    with closing(connection.cursor()) as cursor:
        sql = "SELECT * FROM Security"
        cursor.execute(sql)
        cursor.row_factory = security_factory
        return cursor.fetchall()


def security_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return SecuritySearchItem(**{k: v for k, v in zip(fields, row)})
