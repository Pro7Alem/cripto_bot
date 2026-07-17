def calc_profit(actual_price, cost, fee=0.002):
    # CALCULATE PROFIT INCLUDING FEES
    return (actual_price - cost) / cost - fee


def get_buy_amount(usdt):
    # BINANCE MINIMUM ORDER VALUE
    min_amount = 5

    if usdt < min_amount:
        return 0

    # LIMIT EACH BUY TO 100 USDT
    return 100 if usdt >= 100 else usdt
