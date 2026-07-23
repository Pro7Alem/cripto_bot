import os
import time

from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

BTC_PRECISION = 8
USDT_PRECISION = 2
PRICE_WINDOW = 20
REENTRY_CONFIRM_SECS = 1
REENTRY_WINDOW_SECS = 30
REENTRY_PULLBACK_PERCENT = -0.35
SYMBOL = os.getenv("SYMBOL")


def get_timestamp():
    return int(time.time())
