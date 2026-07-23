from core.utils.config import (
    REENTRY_PULLBACK_PERCENT,
    REENTRY_WINDOW_SECS,
    get_timestamp,
)


def evaluate_reentry(current_price, market_type, prices):
    if market_type != "LATERAL":
        return None

    now = get_timestamp()

    while prices and now - prices[0][0] > REENTRY_WINDOW_SECS:
        prices.popleft()

    if len(prices) < 5:
        return None

    highest_index = max(range(len(prices)), key=lambda i: prices[i][1])
    highest_price = prices[highest_index][1]

    """
    if now - highest_timestamp < REENTRY_CONFIRM_SECS:
        return None
    """

    if highest_index >= len(prices) - 2:
        return None

    pullback = ((current_price - highest_price) / highest_price) * 100

    if pullback <= REENTRY_PULLBACK_PERCENT:
        return {"action": "BUY"}
