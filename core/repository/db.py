import sqlite3

from pathlib import Path
from typing import Any, Dict, List


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "data" / "database.db"


def get_conn():
    # OPEN DATABASE CONNECTION
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn


def exec_query(sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
    # TO SEARCH DATA (SELECT)
    with get_conn() as conn:
        cur = conn.execute(sql, params)

        return [dict(row) for row in cur.fetchall()]


def exec_command(sql: str, params: tuple = ()) -> int:
    # TO SAVE/UPDATE DATA (INSERT, UPDATE, DELETE)
    with get_conn() as conn:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.lastrowid


def create_command(sql: str):
    # TO CREATE TABLES
    with get_conn() as conn:
        cur = conn.execute(sql)
        conn.commit()
        return cur.lastrowid
