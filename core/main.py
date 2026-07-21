import asyncio

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
                decision = None
                msg = await stream.recv()

                if "p" not in msg:
                    print(msg)
                    continue

                price = float(msg["p"])

                # KEEP ONLY THE LAST 20 PRICES
                bot.add_price(price)
                bot.analyze_market()


                decision = bot.evaluate(price)
                
                if decision:
                    await bot.execute(decision)


                bot.log_market(price)
                
                
                update_dashboard(
                    price=price,
                    btc=bot.wallet["btc"],
                    usdt=bot.wallet["usdt"],
                    volatility=bot.market["volatility"],
                    market_type=bot.market["market_type"],
                    prices_count=len(bot.prices)
                )
                

    except Exception as e:
        print("ERROR: ", e)
        await asyncio.sleep(5)

    finally:
        await client.close_connection()


if __name__ == "__main__":
    asyncio.run(main())
