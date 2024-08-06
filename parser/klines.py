import asyncio
from datetime import datetime
import pendulum

from binance.client import AsyncClient

from sqlalchemy.future import select
from sqlalchemy import text

from database.Base import async_connection
from database.models.token import Symbol, Kline

from config import BinanceConfig as Config


async def get_symbols() -> list[Symbol]:
    session, engine = async_connection()
    async with session() as db:
        result = await db.execute(select(Symbol).filter(Symbol.status == 1))
        symbols = [element[0] for element in result.all()]
    await engine.dispose()
    return symbols


async def save_new_klines(symbol: Symbol, klines: list[list], max_time_open: float = 0.0) -> None:
    session, engine = async_connection()
    async with session() as db:
        new_klines = filter(lambda kline: pendulum.from_timestamp(kline[0]/1000, "UTC").naive() > max_time_open, klines)
        klines_for_db = [
            Kline(
                id_symbol=symbol.id,
                open=float(kline[1]),
                high=float(kline[2]),
                low=float(kline[3]),
                close=float(kline[4]),
                volume=float(kline[5]),
                number_of_trades=kline[8],
                time_open=pendulum.from_timestamp(kline[0]/1000, "UTC").naive(),
                time_close=pendulum.from_timestamp(kline[6]/1000, "UTC").naive()
            ) for kline in new_klines if datetime.now() >= datetime.fromtimestamp(kline[6]/1000)
        ]
        db.add_all(klines_for_db)
        await db.commit()
    await engine.dispose()


async def main():
    BinanceAPI = AsyncClient(Config.api_key, Config.api_secret)
    
    sql_query = text(f"""select id_symbol, max(time_open) from kline group by id_symbol""")
    session, engine = async_connection()
    async with session() as db:
        result = await db.execute(sql_query)
        max_time_open_in_db = {element[0]: element[1].timestamp() * 1000 if element[1] else 0 for element in result.all()}

    symbols = await get_symbols()
    for symbol in symbols:
        klines = await BinanceAPI.get_klines(symbol=symbol.symbol, interval="1m", limit=10)
        max_time_open = datetime.fromtimestamp(max_time_open_in_db[symbol.id]/1000 if symbol.id in max_time_open_in_db else 0.0)
        await save_new_klines(symbol, klines, max_time_open)
    
    await BinanceAPI.close_connection()
    await engine.dispose()
    

if __name__ == "__main__":
    asyncio.run(main())
