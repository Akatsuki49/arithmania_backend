import pandas as pd
import numpy as np

url = "https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz"
data = pd.read_csv(url,compression="gzip")
data['name'] = data['name'].astype(str)
new_df = data[['instrument_key','name']]
pattern = 'GOI|SEC|SDL|Nifty|NIFTY|\d|BIRLASLAMC'
clean_df = new_df[new_df['name']!='nan']
clean_df1 = clean_df[~clean_df['name'].str.contains('INR')]
clean_df2 = clean_df1[clean_df1['instrument_key'].str.contains('BSE') | clean_df1['instrument_key'].str.contains('NSE')]
clean_df3 = clean_df2[~clean_df2['name'].str.contains(pattern, regex=True)]
clean_df3.reset_index(drop=True,inplace=True)
clean_df3.to_csv("stocks_raw.csv")