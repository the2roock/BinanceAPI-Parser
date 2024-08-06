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
### Connect to Database
### Parse Tickers
### Parse Candlesticks
