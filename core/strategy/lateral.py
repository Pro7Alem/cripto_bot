from core.strategy.analyzer import analyze_market
from core.utils.trading import calc_profit


COOLDOWN_PRICES = 20


def evaluate_lateral(actual_price, cost, btc, usdt, last_trade_index, prices):
    last_trade_index = last_trade_index or 0

    new_prices_count = len(prices) - last_trade_index

    _, market_type, _ = analyze_market(prices)

    # BUY
    if btc == 0 and usdt > 0 and new_prices_count >= COOLDOWN_PRICES:
        return {"action": "BUY", "last_trade_index": len(prices)}

    # HOLD
    if btc > 0 and cost is None:
        return None

    if btc > 0:
        profit = calc_profit(actual_price, cost)

        # TAKE PROFIT
        if profit >= 0.005:
            return {"action": "SELL", "profit": profit, "last_trade_index": len(prices)}

        # STOP LOSS
        if profit <= -0.003 or (market_type != "lateral" and profit >= 0.002):
            return {"action": "SELL", "profit": profit, "last_trade_index": len(prices)}

    return None
