import asyncio

from core.exchange.client import create_client
from core.exchange.market import create_trade_socket
from core.repository.wallet import get_local_wallet
from core.strategy.analyzer import analyze_market
from core.display.terminal import update_dashboard


PRICE_WINDOW = 20


async def main():
    client = await create_client()

    prices = []

    try:
        socket = create_trade_socket(client)

        async with socket as stream:
            while True:
                msg = await stream.recv()

                price = float(msg["p"])

                prices.append(price)

                # KEEP ONLY THE LAST 20 PRICES
                if len(prices) > PRICE_WINDOW:
                    prices.pop(0)

                volatility, market_type, force = analyze_market(prices)

                wallet = get_local_wallet()

                btc = wallet["btc"]
                usdt = wallet["usdt"]
                cost = wallet["cost"]

                update_dashboard(
                    price=price,
                    btc=btc,
                    usdt=usdt,
                    volatility=volatility,
                    market_type=market_type,
                    prices_count=len(prices)
                )

                await asyncio.sleep(0.1)

    except Exception as e:
        print("ERROR: ", e)

    finally:
        await client.close_connection()


if __name__ == "__main__":
    asyncio.run(main())
