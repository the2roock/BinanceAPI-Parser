# BinanceAPI-Parser
The project on parsing the price data of crypto tokens from the Binance API to be used by trading systems.

## Goal
The main goal of this project is to parse crypto tokens` market data to facilitate usage by trading systems.

## Result
The project successfully parses historical data for BTCUSDT, as illustrated in the plot below:
![BTCUSDT historical data plot](https://github.com/the2roock/BinanceAPI-Parser/blob/main/parser/historical/BTCUSDT_last_180_candles.png)

## Skills Required
- Async Programming
- Python
- API Parsing
- MySQL
- SQLAlchemy
- Pandas

## Understanding Binance API
Binance uses the OAuth 2.0 protocol to access the API, so personal API key and secret are required. For detailed information, refer to the https://developers.binance.com/docs/.
### Endpoints Used:
**- General Info:**
  - GET `/api/v3/exchangeInfo`: Information about tickers. 
**- Market Data:**
  - GET `/api/v3/depth`: Ticker`s order book.
  - GET `/api/v3/klines`: Ticker`s candlesticks.
For more details, visit:
* https://developers.binance.com/docs/binance-spot-api-docs/rest-api#general-endpoints
* https://developers.binance.com/docs/binance-spot-api-docs/rest-api#market-data-endpoints

## Data Description
### Database Structure:
![Database Structure Diagram](https://github.com/the2roock/BinanceAPI-Parser/blob/main/db-diagram.png)

### Tables:
- **symbol**: Ticker model.
  - *id*: `int`
  - *status*: `int` - Ticker`s mark. Option *2* allow ticker for parsers.
  - *symbol*: `varchar(50)` - Ticker`s symbol.
  - *data*: `json` - Additional information about the ticker.
  - *time_create*: `timestamp` - Record creation time.
  - *time_update*: `timestamp` - Record update time.

- **kline**: Candlestick model.
  - *id*: `int`
  - *id_symbol*: `int` - Relation with **symbol** table.
  - *open*: `double` - Candle`s open price.
  - *high*: `double`- Candle`s high price.
  - *low*: `double` - Candle`s low price.
  - *close*: `double` - Candle`s close price.
  - *volume*: `double` - Candle`s volume.
  - *number_of_trades*: `int` - Number of trades.
  - *time_open*: `timestamp` - Candle`s open time.
  - *time_close*: `timestamp` - Candle`s close time.
  - *time_create*: `timestamp` - Record creation time.
  - *time_update*: `timestamp` - Record update time.

- **order_book**: Depth model.
  - *id*: `int`
  - *id_symbol*: `int` - Relation with **symbol** table.
  - *ask*: `text` - Ask levels and their volumes.
  - *bid*: `text` - Bid levels and their volumes.
  - *time_open*: `timestamp` - Binance order book tracking time.
  - *time_create*: `timestamp` - Record creation time.
  - *time_update*: `timestamp` - Record update time.
  
## Usage
### Requirements
First, install the required tools for database management, the binance SDK, Python asyncio and pandas libraries.
```bash
pip install -r requirements.txt
```

### Connect to Database
**Alembic** and **SQLAlchemy** is used to simplify work with database.
1. Create database:
```bash
mysql
```
```sql
CREATE DATABASE binance_parsing;
```
2. Change directory for the next steps:
```bash
cd database
```
3. Create default database migrations package:
```bash
alembic init migrations
```
4. Configure *alembic.ini* and *migrations/env.py* files. Set sqlalchemy_url in alembic.ini. Nesessary imports in *migrations/env.py* are already done but can be modified if needed.
5. Upgrade the database:
```bash
alembic revision --autogenerate -m 'init migrations'
alembic upgrade head
```

### Note
All python scripts are designed to be used from root *BinanceAPI-Parser* directory.

### Parse Tickers
Use *parser/tokens.py* to parse all new tokens:
```bash
python -m parser.tokens
```

### Parse Candlesticks
Use *parser/historical/klines.py* to collect historical price data. Ensure tickers to be parsed have `status = 2` in the database:
```bash
python3 -m parser.history.klines
```

### Create Ticker`s Klines CSV
Use *database/scripts/klines_to_csv.py* to download ticker data from **kline** table:
```bash
python3 -m database.scripts.klines_to_csv 'BTCUSDT'
```
