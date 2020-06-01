import sqlite3


def fetch_conn(db_name: str) -> sqlite3.Connection:
    return sqlite3.connect(db_name)
