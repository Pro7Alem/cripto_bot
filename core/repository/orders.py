import time

from core.repository.db import exec_command


def log_order(order_type, price, quantity, profit=None):
    # SAVE ORDER TO DATABASE
    time_stamp = int(time.time() * 1000)

    exec_command(
        """INSERT INTO orders (
		order_type,
		price_usdt,
		quantity,
		time_stamp,
		profit_percent
	) VALUES (?, ?, ?, ?, ?)""",
        (order_type, price, quantity, time_stamp, profit),
    )
