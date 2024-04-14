import pandas as pd
import numpy as np

url = "https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz"
data = pd.read_csv(url,compression="gzip")
# print(data['last_price'].head(10))
data['name'] = data['name'].astype(str)
unique_names = np.array(data['name'])
names_list_lower = [name.lower() for name in unique_names]
# print(names_list_lower)
new_df = pd.read_csv("top100stocks.csv")
new_df = new_df[['instrument_key','name']]
# new_df = pd.DataFrame(columns=['instrument_key','name'])
for x in names_list_lower:
    if("bharat electronics" in x.lower()):
        ind = names_list_lower.index(x)
        res = data.iloc[ind]
        res = res[['instrument_key','name']]
        print(res)
        new_df.loc[len(new_df)]=res
        break

new_df.to_csv("top100stocks.csv")
# print(new_df)
# print(unique_names)