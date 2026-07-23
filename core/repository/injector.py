from core.repository.db import create_command, exec_command, exec_query
from core.utils.config import get_timestamp


def create_tables():
    # CREATE TABLES IF NOT EXISTS trades AND wallet
    create_command("""CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT,
        order_type TEXT NOT NULL,
        symbol TEXT NOT NULL,
                   
        price_usdt REAL NOT NULL,
        quantity REAL NOT NULL,
                   
        quote_amount REAL NOT NULL,
                   
        fee_asset TEXT,
        fee_amount REAL,
                   
        timestamp INTEGER NOT NULL,
                   
        profit_usdt REAL,
        profit_percent REAL)""")

    create_command("""CREATE TABLE IF NOT EXISTS wallet (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        btc REAL NOT NULL,
        usdt REAL NOT NULL,
        updated_at INTEGER NOT NULL)""")

    create_command("""CREATE TABLE IF NOT EXISTS market_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        price_usdt REAL NOT NULL,
        timestamp INTEGER NOT NULL,
        market_type TEXT,
        volatility REAL,
        force REAL)""")


def init_wallet():
    current_timestamp = get_timestamp()

    wallet = exec_query("SELECT * FROM wallet WHERE id = 1")

    if wallet:
        return wallet[0]

    exec_command(
        """
        INSERT INTO wallet (btc, usdt, updated_at)
        VALUES (?, ?, ?)
        """,
        (0.0, 100.0, current_timestamp),
    )

    wallet = exec_query("SELECT * FROM wallet WHERE id = 1")

    return wallet[0]


create_tables()
print(init_wallet())
