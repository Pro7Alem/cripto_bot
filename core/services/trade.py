from core.exchange.orders import (
    market_buy,
    market_sell,
)
from core.repository.orders import log_order
from core.repository.wallet import update_local_wallet
from core.utils.trading import get_buy_amount


async def buy(client, btc, usdt, cost):

    buy_amount = get_buy_amount(usdt)

    if buy_amount == 0:
        print("[BUY SKIPPED] Insufficient USDT")
        return btc, usdt, cost

    try:
        order = await market_buy(client, buy_amount)

        price = float(order["fills"][0]["price"])
        quantity = float(order["fills"][0]["qty"])

        btc = quantity
        cost = price
        usdt -= buy_amount

        update_local_wallet(btc, usdt, cost)

        log_order("BUY", price, quantity)

    except Exception as e:
        print("BUY ERROR: ", e)

        if "order" in locals():
            print("[WARNING] ORDER MAY HAVE EXECUTED. CHECK EXCHANGE STATE")

        return btc, usdt, cost

    return btc, usdt, cost


async def sell(client, btc, usdt, cost, profit):

    if btc == 0:
        print("[SELL SKIPPED] No BTC to sell")
        return btc, usdt, cost, None

    try:
        # EXECUTE MARKET SELL ORDER
        order = await market_sell(client, btc)

        sell_price = float(order["fills"][0]["price"])
        sold_amount = btc

        usdt += sold_amount * sell_price
        btc = 0
        cost = None

        update_local_wallet(btc, usdt, cost)

        log_order("SELL", sell_price, sold_amount, profit)

    except Exception as e:
        print("SELL ERROR:", e)
        
        return btc, usdt, cost, None

    return btc, usdt, cost, sell_price
