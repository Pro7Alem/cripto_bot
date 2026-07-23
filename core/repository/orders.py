from core.repository.db import exec_command, exec_query
from core.utils.config import get_timestamp


def log_order(
    order_id,
    order_type,
    symbol,
    price,
    quantity,
    quote_amount,
    fee_asset=None,
    fee_amount=None,
    profit_usdt=None,
    profit_percent=None,
):
    # SAVE ORDER TO DATABASE
    current_timestamp = get_timestamp()

    exec_command(
        """INSERT INTO trades (
        order_id,
		order_type,
        symbol,
		price_usdt,
		quantity,
        quote_amount,
        fee_asset,
        fee_amount,
		timestamp,
        profit_usdt,
		profit_percent
	) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            order_id,
            order_type,
            symbol,
            price,
            quantity,
            quote_amount,
            fee_asset,
            fee_amount,
            current_timestamp,
            profit_usdt,
            profit_percent,
        ),
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


def get_last_buy_price():

    result = exec_query(
        """
        SELECT price_usdt
        FROM trades
        WHERE order_type = 'BUY'
        AND id > (
            SELECT id
            FROM trades
            WHERE order_type = 'SELL'
            ORDER BY id DESC
            LIMIT 1
        )
        ORDER BY id DESC
        LIMIT 1
        """
    )

    if not result:
        return None

    return result[0]["price_usdt"]
