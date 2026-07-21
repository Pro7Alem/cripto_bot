from core.repository.market import log_market_price
from core.repository.orders import get_last_sell_trade
from core.services.trade import buy, sell
from core.strategy.analyzer import analyze_market
from core.strategy.lateral import evaluate_lateral
from core.strategy.reentry import evaluate_reentry
from core.utils.config import get_timestamp, PRICE_WINDOW
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

        self.market = {
            "volatility": None,
            "market_type": None,
            "force": None
        }

        self.last_market_log = 0
        self.last_market_price = None

        self.wallet = get_local_wallet()

        last_sell_price = get_last_sell_trade()

        if self.wallet["btc"] == 0 and last_sell_price:
            self.reentry["last_sell_price"] = last_sell_price
            self.reentry["waiting"] = True

    
    def set_reentry(self, waiting, observed_prices, last_sell_price):
        self.reentry["waiting"] = waiting
        self.reentry["observed_prices"] = observed_prices
        self.reentry["last_sell_price"] = last_sell_price


    def set_wallet(self, btc, usdt, cost):
        self.wallet["btc"] = btc
        self.wallet["usdt"] = usdt
        self.wallet["cost"] = cost


    def add_price(self, price):
        self.prices.append(price)

        if len(self.prices) > PRICE_WINDOW:
            self.prices.pop(0)

        if self.reentry["waiting"]:
            self.reentry["observed_prices"] += 1


    def analyze_market(self):
        volatility, market_type, force = analyze_market(self.prices)

        self.market["volatility"] = volatility
        self.market["market_type"] = market_type
        self.market["force"] = force
    

    def evaluate(self, price):
        if self.wallet["btc"] == 0:
            if self.reentry["waiting"]:
                return evaluate_reentry(
                    price,
                    self.reentry["last_sell_price"],
                    self.market["market_type"],
                    self.reentry["observed_prices"]
                )
            
            return evaluate_lateral(
                price,
                self.wallet["cost"],
                self.wallet["btc"],
                self.wallet["usdt"],
                self.market["market_type"]
            )
        
        return evaluate_lateral(
            price,
            self.wallet["cost"],
            self.wallet["btc"],
            self.wallet["usdt"],
            self.market["market_type"]
        )
    

    async def execute_buy(self):
        btc, usdt, cost = await buy(
            self.client,
            self.wallet["btc"],
            self.wallet["usdt"],
            self.wallet["cost"]
        )

        self.set_wallet(btc, usdt, cost)
        self.set_reentry(False, 0, None)
    


    async def execute_sell(self, profit):
        btc, usdt, cost, sell_price = await sell(
            self.client,
            self.wallet["btc"],
            self.wallet["usdt"],
            self.wallet["cost"],
            profit
        )

        self.set_wallet(btc, usdt, cost)

        if sell_price:
            self.set_reentry(True, 0, sell_price)


    async def execute(self, decision):
        if decision["action"] == "BUY":
            await self.execute_buy()

        elif decision["action"] == "SELL":
            await self.execute_sell(decision["profit"])


    def log_market(self, price):
        current_timestamp = get_timestamp()

        if (current_timestamp - self.last_market_log >= 1
            and price != self.last_market_price
            and self.market["market_type"] != "waiting"
            ):
            self.last_market_log, self.last_market_price = log_market_price(
                price,
                self.market["market_type"],
                self.market["volatility"],
                self.market["force"]

            )