import os

from dotenv import load_dotenv


load_dotenv()

SYMBOL = os.getenv("SYMBOL")


async def market_buy(client, quote_amount: float):
    return await client.order_market_buy(
        symbol=SYMBOL,
        quoteOrderQty=quote_amount,
    )


async def market_sell(client, quantity: float):
    return await client.order_market_sell(
        symbol=SYMBOL,
        quantity=quantity,
    )


def get_execution_price(order) -> float:
    return float(order["fills"][0]["price"])


def get_execution_quantity(order) -> float:
    return float(order["fills"][0]["qty"])
