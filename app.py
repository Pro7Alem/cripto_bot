from binance import AsyncClient, BinanceSocketManager
from dotenv import load_dotenv
import os
import asyncio
import sys

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

async def get_market_data(client, symbol="BTCUSDT"):
	
	while True:
		price_btc = float((await client.get_symbol_ticker(symbol="BTCUSDT"))["price"])
		balance_btc = float((await client.get_asset_balance(asset="BTC"))["free"])
		balance_usdt = float((await client.get_asset_balance(asset="USDT"))["free"])
		
		msg = f"BTC Price: {price_btc:.2f} | BTC Balance: {balance_btc} | USDT Balance: {balance_usdt}"
		sys.stdout.write("\r"+msg)
		sys.stdout.flush()
		
		await asyncio.sleep(5)
		
async def get_market_prices(client, symbol="BTCUSDT", n=20, period=3):
	prices = []
	
	for _ in range(n):
		price = float(await client.get_symbol_ticker(symbol=symbol)["price"])
		prices.append(price)
		
		await asyncio.sleep(period)
	
	return prices

async def main():
	client = await AsyncClient.create(API_KEY, API_SECRET, testnet=True)
	
	try:
		await get_market_data(client)
	except Exception as e:
		print("ERRO REAL: ", e)
	finally:
		await client.close_connection()
	
	
if __name__ == "__main__":
	asyncio.run(main())
