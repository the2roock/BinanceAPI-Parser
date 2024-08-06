import asyncio

from binance.client import AsyncClient

from sqlalchemy.future import select

from database.Base import async_connection
from database.models.token import Symbol

from .config import BinanceConfig as Config


async def get_all_symbols_from_db() -> list[str]:
    session, engine = async_connection()
    async with session() as db:
        symbols = await db.execute(select(Symbol))
        all_symbols = [s[0].symbol for s in symbols.all()]
    await engine.dispose()
    return all_symbols


async def save_new_symbols(new_symbols: list[str]) -> None:
    symbols = [
        Symbol(
            symbol=symbol,
            data={
                "src": "binance-api"
            }
        ) for symbol in new_symbols
    ]
    session, engine = async_connection()
    async with session() as db:
        db.add_all(symbols)
        await db.commit()
    await engine.dispose()


async def main():
    BinanceAPI = AsyncClient(Config.api_key, Config.api_secret)
    
    symbols_from_db = await get_all_symbols_from_db()
    symbols_from_binance = await BinanceAPI.get_all_tickers()
    symbols_from_binance = [symbol["symbol"] for symbol in symbols_from_binance]
    new_symbols = list(set(symbols_from_binance) - set(symbols_from_db))
    if new_symbols:
        await save_new_symbols(new_symbols)
    
    await BinanceAPI.close_connection()


if __name__ == "__main__":
    asyncio.run(main())
