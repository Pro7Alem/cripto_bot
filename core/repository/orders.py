from core.repository.db import exec_command, exec_query
from core.utils.config import SYMBOL, get_timestamp


def log_order(order_type, price, quantity, profit=None):
    # SAVE ORDER TO DATABASE

    current_timestamp = get_timestamp()

    exec_command(
        """INSERT INTO trades (
		order_type,
		price_usdt,
		quantity,
		timestamp,
		profit_percent
	) VALUES (?, ?, ?, ?, ?)""",
        (order_type, price, quantity, current_timestamp, profit),
    )


def get_last_sell_trade():
    result = exec_query(
        """SELECT price_usdt
        FROM trades
        WHERE order_type = 'SELL'
        ORDER BY id DESC
        LIMIT 1"""
        )
    
    if not result:
        return None
    
    return result[0]["price_usdt"]