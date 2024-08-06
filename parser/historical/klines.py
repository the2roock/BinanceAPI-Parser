import asyncio
from datetime import datetime
from time import time

from binance.client import AsyncClient

from sqlalchemy.future import select
from sqlalchemy import text

from database.Base import async_connection
from database.models.token import Symbol, Kline

from parser.config import BinanceConfig as Config


async def get_symbols() -> list[Symbol]:
    session, engine = async_connection()
    async with session() as db:
        result = await db.execute(select(Symbol).filter(Symbol.status == 2))
        symbols = [element[0] for element in result.all()]
    await engine.dispose()
    return symbols


async def get_max_time_open_for_symbols(symbols: list[Symbol], time_if_None: int = 0) -> dict[Symbol, int]:
    symbol_ids = tuple(symbol.id for symbol in symbols)
    sql_query = f"""
        select 
            id_symbol,
            max(time_open)
        from (select * from kline where id_symbol in {symbol_ids}) as kline
        group by id_symbol
    """
    session, engine = async_connection()
    async with session() as db:
        result = await db.execute(text(sql_query))
        max_time_open = {
            element[0]: element[1]
            for element in result.all()
        }
    await engine.dispose()
    symbol_max_time_open = {symbol: int(max_time_open[symbol.id].timestamp()*1000) if symbol.id in max_time_open else time_if_None for symbol in symbols}
    return symbol_max_time_open


async def save_into_db(klines: list[Kline]):
    session, engine = async_connection()
    async with session() as db:
        db.add_all(klines)
        await db.commit()
    await engine.dispose()
    

async def main():
    BinanceAPI = AsyncClient(Config.api_key, Config.api_secret)
    
    symbols = await get_symbols()
    
    min_timestamp = 0
    max_saved_time_opens = await get_max_time_open_for_symbols(symbols=symbols, time_if_None=min_timestamp)
    
    for symbol, start_timestamp in max_saved_time_opens.items():
        klines_row = list()
        start_timestamp += 60 * 1000    # increment 60 seconds
        
        # test start_timestamp
        klines = await BinanceAPI.get_klines(symbol=symbol.symbol, interval="1m", startTime=start_timestamp, limit=100)
        try:
            if start_timestamp < klines[0][0]:
                start_timestamp = klines[0][0]
                print(f"start time is confused and set to {datetime.fromtimestamp(start_timestamp/1000)}")
        except Exception as e:
            print(f"The symbol {symbol.symbol} is broken: {e}\n")
            continue
        
        print(f"Downloading {symbol.symbol} data starts from {datetime.fromtimestamp(start_timestamp / 1000)}")
        t0 = time()    
        while start_timestamp < datetime.now().timestamp() * 1000:
            end_timestamp = start_timestamp + 1000 * 60 * 1000
            klines = await BinanceAPI.get_klines(symbol=symbol.symbol, interval="1m", startTime=start_timestamp, endTime=end_timestamp, limit=1000)
            print('time:', datetime.fromtimestamp(start_timestamp/1000), '--', datetime.fromtimestamp(end_timestamp/1000), 'length of data:', len(klines), end='\r')
            
            start_timestamp = end_timestamp
            klines_row.extend(klines)
            
            klines_db = [
                Kline(
                    id_symbol=symbol.id,
                    open=float(kline[1]),
                    high=float(kline[2]),
                    low=float(kline[3]),
                    close=float(kline[4]),
                    volume=float(kline[5]),
                    number_of_trades=kline[8],
                    time_open=datetime.fromtimestamp(kline[0]/1000).replace(microsecond=0),
                    time_close=datetime.fromtimestamp(kline[6]/1000).replace(microsecond=0)
                )
                for kline in klines
            ]
            await save_into_db(klines=klines_db)
            
        print(f"Data is downloaded. Time spent - {round(time() - t0, 2)}s\n")
        
    await BinanceAPI.close_connection()
    
        

if __name__ == "__main__":
    asyncio.run(main())
