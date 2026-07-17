import os

from dotenv import load_dotenv
from core.exchange.client import create_socket_manager


load_dotenv()

SYMBOL = os.getenv("SYMBOL")


def create_trade_socket(client):
    bsm = create_socket_manager(client)

    return bsm.trade_socket(SYMBOL)
