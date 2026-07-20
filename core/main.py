import asyncio

from core.bot.trading_bot import TradingBot
from core.display.terminal import update_dashboard
from core.exchange.client import create_client
from core.exchange.market import create_trade_socket
from core.repository.market import log_market_price
from core.repository.orders import get_last_sell_trade
from core.repository.wallet import get_local_wallet
from core.services.trade import buy, sell
from core.strategy.analyzer import analyze_market
from core.strategy.lateral import evaluate_lateral
from core.strategy.reentry import evaluate_reentry
from core.utils.config import PRICE_WINDOW, get_timestamp


async def main():
    client = await create_client()
    bot = TradingBot(client)

    prices = []

    reentry = {
        "observed_prices": 0,
        "waiting": False,
        "last_sell_price": None
    }

    last_sell_price = get_last_sell_trade()
    wallet = get_local_wallet()

    if wallet["btc"] == 0 and last_sell_price:
        reentry["last_sell_price"] = last_sell_price
        reentry["waiting"] = True

    last_market_log = 0
    last_market_price = None

    try:
        socket = create_trade_socket(client)

        async with socket as stream:
            while True:
                decision = None
                msg = await stream.recv()

                if "p" not in msg:
                    print(msg)
                    continue

                price = float(msg["p"])

                prices.append(price)

                if reentry["waiting"]:
                    reentry["observed_prices"] += 1

                # KEEP ONLY THE LAST 20 PRICES
                if len(prices) > PRICE_WINDOW:
                    prices.pop(0)

                volatility, market_type, force = analyze_market(prices)

                wallet = get_local_wallet()

                btc = wallet["btc"]
                usdt = wallet["usdt"]
                cost = wallet["cost"]

                # await asyncio.sleep(0.1)

                if btc == 0:
                    if reentry["waiting"]:
                        decision = evaluate_reentry(
                            price,
                            reentry["last_sell_price"],
                            market_type,
                            reentry["observed_prices"]
                            )
                    else:
                        decision = evaluate_lateral(
                            price,
                            cost,
                            btc,
                            usdt,
                            market_type
                        )
                else:
                    decision = evaluate_lateral(
                        price,
                        cost,
                        btc,
                        usdt,
                        market_type
                    )

                
                if decision:
                    if decision["action"] == "BUY":
                        btc, usdt, cost = await buy(
                            client,
                            btc,
                            usdt,
                            cost
                        )

                        reentry["waiting"] = False
                        reentry["observed_prices"] = 0
                        reentry["last_sell_price"] = None

                    elif decision["action"] == "SELL":
                        btc, usdt, cost, sell_price = await sell(
                            client,
                            btc,
                            usdt,
                            cost,
                            decision["profit"]
                        )
                        if sell_price:
                            reentry["waiting"] = True
                            reentry["observed_prices"] = 0
                            reentry["last_sell_price"] = sell_price
                
                current_timestamp = get_timestamp()

                if (current_timestamp - last_market_log >= 1
                    and price != last_market_price
                    ):
                    last_market_log, last_market_price = log_market_price(
                        price,
                        market_type,
                        volatility,
                        force
                    )
                
                update_dashboard(
                    price=price,
                    btc=btc,
                    usdt=usdt,
                    volatility=volatility,
                    market_type=market_type,
                    prices_count=len(prices)
                )
                

    except Exception as e:
        print("ERROR: ", e)
        await asyncio.sleep(5)

    finally:
        await client.close_connection()


if __name__ == "__main__":
    asyncio.run(main())
