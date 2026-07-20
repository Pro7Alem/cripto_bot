from core.repository.db import exec_query, exec_command
from core.utils.config import REENTRY_DROP_PERCENT, REENTRY_MIN_PRICES


def evaluate_reentry(current_price, last_sell_price, market_type, new_prices_observed):
    if last_sell_price is None:
        return None

    if new_prices_observed < REENTRY_MIN_PRICES:
        return None
    
    if market_type != "LATERAL":
        return None
    
    pct_change = ((current_price - last_sell_price) / last_sell_price) * 100

    if pct_change <= REENTRY_DROP_PERCENT:
        return {"action": "BUY"}

    