# BinanceAPI-Parser
The project on crypto tokens` price parsing from binance-api

## Goal
The project focuses on parsing crypto tokens` market data be able to use by trading systems.

## Skills Required
- Async Programming
- Python
- API Parsing
- MySQL
- SQLAlchemy
- Pandas

## Understanding Binance API
Binance uses OAuth 2.0 protocol to access the API, so personal API key and secret are required. There is more detailed info https://developers.binance.com/docs/.
Next endpoints are used in the project:
### - General Info:
  - GET `/api/v3/exchangeInfo`: info about tickers. 
### - Market Data:
  - GET `/api/v3/depth`: ticker`s order book.
  - GET `/api/v3/klines`: ticker`s candlesticks.
For more details use https://developers.binance.com/docs/binance-spot-api-docs/rest-api#general-endpoints and https://developers.binance.com/docs/binance-spot-api-docs/rest-api#market-data-endpoints

## Data Description
### Database Structure:
![Database Structure Diagram](https://github.com/the2roock/BinanceAPI-Parser/blob/main/db-diagram.png)

### Tables:
- **symbol**: Ticker model.
  - *id*: `int`
  - *status*: `int` - ticker`s mark. Option *2* marks ticker for parsers.
  - *symbol*: `varchar(50)` - ticker`s symbol.
  - *data*: `json` - anything about ticker. Data source for example.
  - *time_create*: `timestamp` - time when record was created.
  - *time_update*: `timestamp` - time when record was updated.

- **kline**: Candlestick model.
  - *id*: `int`
  - *id_symbol*: `int` - relation w/ **symbol** table.
  - *open*: `double` - candle`s open.
  - *high*: `double`- candle`s high.
  - *low*: `double` - candle`s low.
  - *close*: `double` - candle`s close.
  - *volume*: `double` - candle`s volume.
  - *number_of_trades*: `int` - candle`s number of trades.
  - *time_open*: `timestamp` - candle`s open time.
  - *time_close*: `timestamp` - candle`s close time.
  - *time_create*: `timestamp` - time when record was created.
  - *time_update*: `timestamp` - time when record was updated.

- **order_book**: Depth model.
  - *id*: `int`
  - *id_symbol*: `int` - relation w/ **symbol** table.
  - *ask*: `text` - combination of ask levels and its volumes written in text form.
  - *bid*: `text` - combination of bid levels and its volumes written in text form.
  - *time_open*: `timestamp` - binance order book`s tracking time.
  - *time_create*: `timestamp` - time when record was created.
  - *time_update*: `timestamp` - time when record was updated.
  
## Usage
### Requirements
First of all need to install requirements such as tools for database management, binance SDK, python asyncio and pandas libraries.
```bash
pip install -r requirements.txt
```

### Connect to Database
The **alembic** and **SQLAlchemy** is used to simplify work with database.
1. Create database:
```bash
mysql
```
```sql
CREATE DATABASE binance_parsing;
```
2. Nedd to change directory for next steps:
```bash
cd database
```
3. Create default database migrations package:
```bash
alembic init migrations
```
4. Configure *alembic.ini* and *migrations/env.py* files. In this step user should set `sqlalchemy_url` in alembic.ini. All nesessary imports in *migrations/env.py* has already done but its be able to change still.
5. Upgrade database:
```bash
alembic revision --autogenerate -m 'init migration'
alembic upgrade head
```

### Parse Tickers
The *parser/tokens.py* is used for parsing all new tokens.
```bash
python -m parser.tokens
```

### Parse Candlesticks
The *parser/historical/klines.py* is used for collecting historical price data. Previously should choose tickers to parse making them `status = 2` in database.
```bash
python3 -m parser.history.klines
```

### Create Ticker`s Klines CSV
The *database/scripts/klines_to_csv.py* is developed for downloading ticker`s data from **kline** table.
```bash
python3 -m database.scripts.klines_to_csv 'BTCUSDT'
```

### Nessesary
All python scripts are designed to be used from root *BinanceAPI-Parser* directory.
