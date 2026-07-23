from decimal import Decimal, ROUND_DOWN


def calc_profit(actual_price, cost, fee=0.002):
    # CALCULATE PROFIT INCLUDING FEES
    return (actual_price - cost) / cost - fee


def get_buy_amount(usdt):
    min_amount = Decimal("5")

    usdt = Decimal(str(usdt))

    if usdt < min_amount:
        return 0

    amount = min(usdt, Decimal("100"))

    return float(amount.quantize(Decimal("0.01"), rounding=ROUND_DOWN))
