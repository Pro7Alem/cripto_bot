from binance import AsyncClient, BinanceSocketManager
from core.utils.config import API_KEY, API_SECRET


async def create_client():
    return await AsyncClient.create(API_KEY, API_SECRET, testnet=True)


def create_socket_manager(client):
    return BinanceSocketManager(client)


async def close_client(client):
    await client.close_connection()
