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
- General Info:
  - GET `/api/v3/exchangeInfo`: info about tickers. 
- Market Data:
  - GET `/api/v3/depth`: ticker`s order book.
  - GET `/api/v3/klines`: ticker`s candlesticks.
For more details use https://developers.binance.com/docs/binance-spot-api-docs/rest-api#general-endpoints and https://developers.binance.com/docs/binance-spot-api-docs/rest-api#market-data-endpoints

## Data Description

## Usage Examples
