import sys


def update_dashboard(
        price,
        btc,
        usdt, 
        volatility,
        market_type,
        prices_count,
        loop_time
):
    if prices_count < 20:
        market_display = f"WAITING DATA ({prices_count}/20)"
    else:
        market_display = market_type


    dashboard = f"""
================ BTC BOT ================

BTC PRICE:       {price:.2f}
BTC BALANCE:     {btc:.8f}
USDT BALANCE:    {usdt:.2f}

VOLATILITY:      {volatility:.2f}%
MARKET:          {market_display:<25}
SLOW LOOP:       {loop_time:<25}

==========================================
"""

    sys.stdout.write("\033[H")
    sys.stdout.write(dashboard)
    sys.stdout.flush()
