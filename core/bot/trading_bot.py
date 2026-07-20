from core.repository.orders import get_last_sell_trade
from core.repository.wallet import get_local_wallet


class TradingBot:

    def __init__(self, client):
        self.client = client

        self.prices = []

        self.reentry = {
            "observed_prices": 0,
            "waiting": False,
            "last_sell_price": None
        }

        self.last_market_log = 0
        self.last_market_price = None

        self.wallet = get_local_wallet()

        last_sell_price = get_last_sell_trade()

        if self.wallet["btc"] == 0 and last_sell_price:
            self.reentry["last_sell_price"] = last_sell_price
            self.reentry["waiting"] = True