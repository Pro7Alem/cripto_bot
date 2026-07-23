import asyncio
import time

from core.bot.trading_bot import TradingBot
from core.display.terminal import update_dashboard
from core.exchange.client import create_client
from core.exchange.market import create_trade_socket


async def main():
    client = await create_client()
    bot = TradingBot(client)

    try:
        socket = create_trade_socket(client)

        async with socket as stream:
            while True:
                start = time.time()
                msg = await stream.recv()

                if "p" not in msg:
                    continue

                price = float(msg["p"])

                # KEEP ONLY THE LAST 20 PRICES
                bot.add_price(price)
                bot.analyze_market()

                decision = bot.evaluate(price)

                if decision:
                    await bot.execute(decision)

                bot.log_market(price)

                elapsed = time.time() - start

                update_dashboard(
                    price=price,
                    btc=bot.wallet["btc"],
                    usdt=bot.wallet["usdt"],
                    volatility=bot.market["volatility"],
                    market_type=bot.market["market_type"],
                    prices_count=len(bot.prices),
                    loop_time=elapsed,
                )

    except Exception as e:
        print("ERROR: ", e)
        await asyncio.sleep(5)

    finally:
        await client.close_connection()


if __name__ == "__main__":
    asyncio.run(main())
