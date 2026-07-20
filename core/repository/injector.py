from core.repository.db import create_command, exec_command, exec_query


def create_tables():
    # CREATE TABLES IF NOT EXISTS trades AND wallet
    create_command("""CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_type TEXT NOT NULL,
        price_usdt REAL NOT NULL,
        quantity REAL NOT NULL,
        timestamp INTEGER NOT NULL,
        profit_percent REAL)""")

    create_command("""CREATE TABLE IF NOT EXISTS wallet (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        btc REAL,
        usdt REAL,
        cost REAL)""")
    
    create_command("""CREATE TABLE IF NOT EXISTS market_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        price_usdt REAL NOT NULL,
        timestamp INTEGER NOT NULL,
        market_type TEXT,
        volatility REAL,
        force REAL)""")


def init_wallet() -> None:
    # INSERT INITIAL VALUES INTO WALLET
    exec_command(
        """INSERT INTO wallet (btc, usdt, cost) VALUES (?, ?, ?)""", (0.0, 100.0, 0.0)
    )

    wallet = exec_query("SELECT * FROM wallet WHERE id = 1")

    return wallet[0] if wallet else None


create_tables()
print(init_wallet())
