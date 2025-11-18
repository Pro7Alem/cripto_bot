import sqlite3

def get_conn():
    conn = sqlite3.connect("data_base.db")
    conn.row_factory = sqlite3.Row

    return conn

conn = get_conn()
cur = conn.cursor()

# cur.execute("""
# CREATE TABLE IF NOT EXISTS orders (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     order_type TEXT NOT NULL,
#     price_usdt REAL NOT NULL,
#     quantity REAL NOT NULL,
#     timestamp INTEGER NOT NULL,
#     profit_percent REAL
# )
# """)

# cur.execute("DROP TABLE wallet")

# cur.execute("""
# CREATE TABLE IF NOT EXISTS wallet (
#     btc REAL,
#     usdt REAL,
#     cost REAL
# )
# """)

cur.execute("UPDATE wallet SET cost=0")



conn.commit()
conn.close()