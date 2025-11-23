from time import sleep

from binance import AsyncClient, BinanceSocketManager
from dotenv import load_dotenv
from data import get_conn
from datetime import datetime
import sqlite3
import os
import asyncio
import sys
import time

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
COOLDOWN_PRICES = 20


async def sell_order(client, btc, usdt, cost, profit):
	conn = get_conn()
	cur = conn.cursor()
	sell_price = None

	try:
		order = await client.order_market_sell(symbol="BTCUSDT", quantity=btc)
		sell_price = float(order["fills"][0]["price"])

		sold_amount = btc
		usdt += btc * sell_price
		btc = 0
		cost = None

		log_order(cur, "SELL", sell_price, sold_amount, profit)
		conn.commit()

	except Exception as e:
		print("ERRO REAL: ", e)

	finally:
		conn.close()

	return btc, usdt, cost, sell_price

async def buy_order(client, btc, usdt, cost):
	conn = get_conn()
	cur = conn.cursor()
	buy_amount = get_buy_amount(usdt)

	if buy_amount == 0:
		print("[BUY SKIPPED] Insufficient USDT")

		return btc, usdt, cost

	try:
		order = await client.order_market_buy(symbol="BTCUSDT", quoteOrderQty=buy_amount)
		cost = float(order["fills"][0]["price"])
		btc = float(order["fills"][0]["qty"])

		usdt -= buy_amount

		log_order(cur, "BUY", cost, btc)
		conn.commit()

	except Exception as e:
		print("ERRO REAL: ", e)
		return btc, usdt, cost

	finally:
		conn.close()

	return btc, usdt, cost

def log_order(cur, order_type, price, quantity, profit=None):
	time_stamp = int(time.time() * 1000)
	cur.execute("""INSERT INTO orders (order_type, price_usdt, quantity, time_stamp, profit_percent)
	                   VALUES (?, ?, ?, ?, ?)""", (order_type, price, quantity, time_stamp, profit))
	cur.connection.commit()

def get_buy_amount(usdt):
	min_amount = 5
	if usdt < min_amount:

		return 0

	return 100 if usdt >= 100 else usdt

def calc_profit(actual_price, cost, fee=0.002):
	return (actual_price - cost) / cost - fee

def get_local_wallet():
	conn = get_conn()
	cur = conn.cursor()

	cur.execute("SELECT btc, usdt, cost FROM wallet LIMIT 1")
	btc, usdt, cost = cur.fetchone()
	return btc, usdt, cost

def update_local_wallet(btc, usdt, cost):
	conn = get_conn()
	cur = conn.cursor()

	cur.execute("UPDATE wallet SET btc = ?, usdt = ?, cost = ?", (btc, usdt, cost))
	conn.commit()


async def analyze_market(prices):
	if len(prices) < 20:
		return 0, "Coletando dados..."
	price_min = min(prices)
	price_max = max(prices)
	price_now = prices[-1]
	volatility = ((price_max - price_min) / price_now) * 100
	force = None

	if volatility < 0.5:
		market_type = "lateral"
	elif volatility > 1.5:
		slope = ((prices[-1] - prices[0]) / prices[0])* 100
		force = ("weak" if abs(slope) < 0.3 else
				 "medium" if abs(slope) < 0.7 else
				 "strong")
			 
		if prices[-1] > prices[0]:
			market_type = "volatile-uptrend"
		else:
			market_type = "volatile-downtrend"
	else:
		market_type = "moderate"

	return volatility, market_type, force

async def strategy_lateral(client, actual_price, cost, btc, usdt, last_trade_index, prices):
	last_trade_index = last_trade_index or 0
	new_prices_count = len(prices) - last_trade_index
	_, market_type, _ = await analyze_market(prices)

	# STARTER BUY
	if btc == 0 and usdt > 0 and new_prices_count >= COOLDOWN_PRICES:
		btc, usdt, cost = await buy_order(client, btc, usdt, cost)
		last_trade_index = len(prices)
		print(f"[BUY] BTC={btc}, USDT={usdt}, Price={cost}")

		return btc, usdt, cost, last_trade_index

	# IF ALREADY HAVE BTC
	if btc > 0:
		if cost is None:
			return btc, usdt, cost, last_trade_index
		else:
			profit = calc_profit(actual_price, cost)

		# TAKE PROFIT
		if profit >= 0.005:

			# SELL ALL BTC
			btc, usdt, cost, sell_price = await sell_order(client, btc, usdt, cost, profit)
			last_trade_index = len(prices)

			# BUYBACK USING AVAILABLE BALANCE
			if usdt > 0 and new_prices_count >= COOLDOWN_PRICES:
				btc, usdt, cost = await buy_order(client, btc, usdt, cost)
				last_trade_index = len(prices)

				print(f"[BUYBACK] BTC={btc}, USDT={usdt}, Price={cost}")

			return btc, usdt, cost, last_trade_index

		# STOP LOSS
		if profit <= -0.003 or (market_type != "lateral" and profit >= 0.002):
			btc, usdt, cost, sell_price = await sell_order(client, btc, usdt, cost, profit)
			last_trade_index = len(prices)

			print(f"[STOP LOSS] BTC vendido, USDT={usdt}")

			return btc, usdt, cost, last_trade_index

	# NO ACTION
	return btc, usdt, cost, last_trade_index




async def main():
	client = await AsyncClient.create(API_KEY, API_SECRET, testnet=True)
	bsm = BinanceSocketManager(client)

	socket = bsm.trade_socket("BTCUSDT")

	prices = []
	last_trade_index = 0

	try:
		async with socket as stream:
			while True:
				msg = await stream.recv()

				price = float(msg["p"])
				prices.append(price)

				if len(prices) > 20:
					prices.pop(0)

				volatility, market_type, force = await analyze_market(prices)

				local_btc, local_usdt, cost = get_local_wallet()

				local_btc, local_usdt, cost, last_trade_index = await strategy_lateral(
					client,
					actual_price=price,
					cost=cost,
					btc=local_btc,
					usdt=local_usdt,
					last_trade_index=last_trade_index,
					prices=prices
				)
				update_local_wallet(local_btc, local_usdt, cost)

				log = (f"Price BTC: {price:.2f} | Local BTC: {local_btc:.8f} | "
					   f"Local USDT: {local_usdt:.2f} | Vol: {volatility:.2f}% | "
					   f"Market: {market_type}")

				sys.stdout.write("\r" + " " * 300 + "\r")
				sys.stdout.write(log)
				sys.stdout.flush()

				await asyncio.sleep(0.1)

	except Exception as e:
		print("ERRO REAL: ", e)
	finally:
		await client.close_connection()
	
	
if __name__ == "__main__":
	asyncio.run(main())
