import asyncio
from datetime import datetime
import pytz
import traceback

from binance.client import AsyncClient

from sqlalchemy.future import select
from sqlalchemy import text

from database.Base import async_connection
from database.models.token import Symbol, OrderBook

from config import BinanceConfig as Config


async def get_symbols() -> list[Symbol]:
    session, engine = async_connection()
    async with session() as db:
        result = await db.execute(select(Symbol).filter(Symbol.status == 1))
        symbols = [element[0] for element in result.all()]
    await engine.dispose()
    return symbols


async def save_depths(symbol: Symbol, order_book: list[list], time_open: float = 0.0) -> None:
    session, engine = async_connection()
    async with session() as db:
        depth_for_db = OrderBook(
                id_symbol=symbol.id,
                ask=order_book["ask"],
                bid=order_book["bid"],
                time_open=time_open
            )
        db.add(depth_for_db)
        await db.commit()
    await engine.dispose()


async def main():
    BinanceAPI = AsyncClient(Config.api_key, Config.api_secret)
    
    time_open = datetime.now(pytz.utc).replace(second=0, microsecond=0, tzinfo=None)
    symbols = await get_symbols()
    
    for symbol in symbols:
        depth = await BinanceAPI.get_order_book(symbol=symbol.symbol, limit=1000)
        order_book = {
            "bid": " ".join([f"{float(element[0])}:{float(element[1])}" for element in depth["bids"][::-1]]),
            "ask": " ".join([f"{float(element[0])}:{float(element[1])}" for element in depth["asks"]]),
        }
        await save_depths(symbol, order_book, time_open)
    
    await BinanceAPI.close_connection()
    

if __name__ == "__main__":
    asyncio.run(main())
