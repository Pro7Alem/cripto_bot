from core.exchange.orders import (
    market_buy,
    market_sell,
)
from core.repository.orders import log_order
from core.repository.wallet import update_local_wallet
from core.utils.config import get_timestamp
from core.utils.trading import get_buy_amount


async def buy(client, btc, usdt, cost):

    buy_amount = get_buy_amount(usdt)

    if buy_amount == 0:
        print("[BUY SKIPPED] Insufficient USDT")
        return btc, usdt, cost

    try:
        order = await market_buy(client, buy_amount)

        price, quantity, quote_amount, fee_asset, fee_amount = parse_order(order)

        btc += quantity
        usdt -= quote_amount
        cost = price
        updated_at = get_timestamp()

        update_local_wallet(btc, usdt, updated_at)

        log_order(
            order_id=order["orderId"],
            order_type="BUY",
            symbol=order["symbol"],
            price=price,
            quantity=quantity,
            quote_amount=quote_amount,
            fee_asset=fee_asset,
            fee_amount=fee_amount,
        )

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

        sell_price, sold_amount, quote_amount, fee_asset, fee_amount = parse_order(
            order
        )

        # REAL PROFIT
        invested = sold_amount * cost

        profit_usdt = quote_amount - invested
        profit_percent = profit_usdt / invested

        usdt += quote_amount
        btc = 0
        cost = None
        updated_at = get_timestamp()

        update_local_wallet(btc, usdt, updated_at)

        log_order(
            order_id=order["orderId"],
            order_type="SELL",
            symbol=order["symbol"],
            price=sell_price,
            quantity=sold_amount,
            quote_amount=quote_amount,
            fee_asset=fee_asset,
            fee_amount=fee_amount,
            profit_usdt=profit_usdt,
            profit_percent=profit_percent,
        )

    except Exception as e:
        print("SELL ERROR:", e)

        return btc, usdt, cost, None

    return btc, usdt, cost, sell_price


def parse_order(order):
    fills = order["fills"]

    quantity = sum(float(fill["qty"]) for fill in fills)

    quote_amount = sum(float(fill["price"]) * float(fill["qty"]) for fill in fills)

    fee_amount = sum(float(fill["commission"]) for fill in fills)

    fee_asset = fills[0]["commissionAsset"]

    price = quote_amount / quantity

    return price, quantity, quote_amount, fee_asset, fee_amount
