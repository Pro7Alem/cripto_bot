from core.repository.db import exec_command
from core.utils.config import get_timestamp, SYMBOL


def log_market_price(price, market_type, volatility, force):
    current_timestamp = get_timestamp()

    exec_command(
        """INSERT INTO market_prices (
        symbol,
        price_usdt,
        timestamp,
        market_type,
        volatility,
        force
    ) VALUES (?, ?, ?, ?, ?, ?)""",
        (SYMBOL, price, current_timestamp, market_type, volatility, force),
    )

    return current_timestamp, price