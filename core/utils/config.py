import os
import time

from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

PRICE_WINDOW = 20
REENTRY_MIN_PRICES = 50
REENTRY_DROP_PERCENT = -5.0
SYMBOL = os.getenv("SYMBOL")


def get_timestamp():
    return int(time.time())