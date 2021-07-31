
import pandas as pd
from datetime import datetime as dt

FILENAME = "test_SPY.txt"

df = pd.read_csv(FILENAME)
df = df.drop(["Date","Open","High","Low","Adj Close","Volume"], axis=1)
df.index = df.index + 1

df.to_csv(FILENAME, header=False, index=True, sep=' ')

# python3 test_rewirte_stock_data.py
