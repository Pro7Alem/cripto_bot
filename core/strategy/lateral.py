from core.utils.trading import calc_profit


def evaluate_lateral(actual_price, cost, btc, usdt, market_type):
    # FIRST BUY
    if btc == 0 and usdt > 0:
        return {"action": "BUY"}

    # HOLD
    if btc > 0 and cost is None:
        return None

    profit = calc_profit(actual_price, cost)

    # TAKE PROFIT
    if profit >= 0.005:
        return {"action": "SELL", "profit": profit}

    # STOP LOSS
    if profit <= -0.003 or (market_type != "LATERAL" and profit >= 0.002):
        return {"action": "SELL", "profit": profit}

    return None
