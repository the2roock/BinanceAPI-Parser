import sys
import os

import pandas as pd

from ..Base import connection
from ..models.token import Symbol, Kline


symbol = sys.argv[1]

db = connection()

symbol = db.query(Symbol).filter(Symbol.symbol == symbol).one_or_none()
if not symbol:
    print("Symbol not found. Please be shure you are using 'python3 -m database.scripts.klines_to_csv \"BTCUSDT\"'.")
    exit()    

klines = db.query(Kline).filter(Kline.id_symbol == symbol.id).all()
print(f"{symbol.symbol}`s data is loaded.")

# Creating and cleaning df
df = pd.DataFrame([kline.__dict__ for kline in klines])

df.drop("_sa_instance_state", axis=1, inplace=True)
db.close()

df.drop("id", axis=1, inplace=True)
df.drop("id_symbol", axis=1, inplace=True)
df.drop("time_create", axis=1, inplace=True)
df.drop("time_update", axis=1, inplace=True)
df.drop("time_close", axis=1, inplace=True)

df.rename(columns={"open": "Open"}, inplace=True)
df.rename(columns={"high": "High"}, inplace=True)
df.rename(columns={"low": "Low"}, inplace=True)
df.rename(columns={"close": "Close"}, inplace=True)
df.rename(columns={"volume": "Volume"}, inplace=True)


df.time_open = pd.to_datetime(df.time_open)
df.set_index("time_open", inplace=True)

print("Dataframe is created.")

# Cleaning data in df

print("Data Checks:")
# duplicates
print("1. Track duplicates ...")
duplicates = len(df) - len(df.drop_duplicates())
df.drop_duplicates(inplace=True)
index_duplicates = sum(df.index.duplicated())
df = df.groupby(df.index).mean()
print(f"Duplicated rows: {duplicates}({round(duplicates / len(df) * 100, 2)}%) are dropped.",
      f"\nDuplicated indexes: {index_duplicates}({round(100 * index_duplicates / len(df), 2)}%) are averaged.")

# is data complete
print("2. Is data complete ...")
all_timestamps = pd.date_range(start=df.index.min(), end=df.index.max(), freq="min")
if len(all_timestamps) != len(df):
    missing_timestamps = len(all_timestamps.difference(df.index))
    df = df.resample('min').asfreq().ffill()
    print(f"There are {missing_timestamps}({round(100 * missing_timestamps / len(df), 2)}%) missing candles. Filled using 'forward fill' method.")
else:
    print("Data is complete.")

# how is data long
duration = df.index[-1] - df.index[0]
print(f"3. Data`s duration is {duration.total_seconds() / (365 * 24 * 3600)} years.")

print(df.info())
print(df.describe())

# Writing in file
dirname = "csv_data"
if not os.path.exists(dirname):
    os.mkdir(dirname)
filename = os.path.join(dirname, f"{symbol.symbol}.csv")
df.to_csv(filename)
