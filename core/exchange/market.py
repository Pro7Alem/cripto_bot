from core.exchange.client import create_socket_manager
from core.utils.config import SYMBOL


def create_trade_socket(client):
    bsm = create_socket_manager(client)

    return bsm.trade_socket(SYMBOL)
