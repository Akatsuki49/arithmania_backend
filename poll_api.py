# import requests
# import pandas as pd
# import json
# import time
# from langchain.document_loaders import CSVLoader
# from datetime import datetime, timedelta
# from dateutil.relativedelta import relativedelta
# from langchain_community.embeddings import OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS
# import os
# import logging

# current_date = datetime.now().date()
# # access_token="eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI1UUFNOFAiLCJqdGkiOiI2NjFiMWMzODc5ZTMxZTNjNmNlMmQ4NjciLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaXNBY3RpdmUiOnRydWUsInNjb3BlIjpbImludGVyYWN0aXZlIiwiaGlzdG9yaWNhbCJdLCJpYXQiOjE3MTMwNTI3MjgsImlzcyI6InVkYXBpLWdhdGV3YXktc2VydmljZSIsImV4cCI6MTcxMzEzMjAwMH0.0uWuMeegluQvYvkf-u3WEgFj30Zm0p_X510Hiuk9JPY"

# def minutewise(id):
#     previous_date1 = current_date - timedelta(days=1)
#     previous_date = previous_date1.strftime('%Y-%m-%d')
#     url = f"https://api.upstox.com/v2/historical-candle/{id}/1minute/{current_date}"
#     headers = {'Accept': 'application/json'}
#     payload = {}
#     print(url)
#     response = requests.request("GET", url, headers=headers, data=payload)
#     print(response.text)
#     r1 = json.loads(response.text)
#     if r1.get("status") == "success" and r1.get("data", {}).get("candles"):
#         candles = r1["data"]["candles"]
#         if len(candles) != 0:
#             return candles[0][2], candles[0][3]
#     return "", ""

# def daywise(id):
#     current_date1 = current_date - timedelta(days=1)
#     current_date2 = current_date1.strftime('%Y-%m-%d')
#     previous_date1 = current_date1 - timedelta(days=2)
#     previous_date = previous_date1.strftime('%Y-%m-%d')
#     url = f"https://api.upstox.com/v2/historical-candle/{id}/day/{current_date2}/{previous_date}"
#     headers = {'Accept': 'application/json'}
#     payload = {}
#     print(url)
#     response = requests.request("GET", url, headers=headers, data=payload)
#     print(response.text)
#     r1 = json.loads(response.text)
#     if r1.get("status") == "success" and r1.get("data", {}).get("candles"):
#         candles = r1["data"]["candles"]
#         if len(candles) != 0:
#             return candles[0][2], candles[0][3]
#     return "", ""

# def weekly(id):
#     previous_date1 = current_date - timedelta(days=7)
#     previous_date = previous_date1.strftime('%Y-%m-%d')
#     url = f"https://api.upstox.com/v2/historical-candle/{id}/week/{current_date}/{previous_date}"
#     headers = {'Accept': 'application/json'}
#     payload = {}
#     print(url)
#     response = requests.request("GET", url, headers=headers, data=payload)
#     print(response.text)
#     r1 = json.loads(response.text)
#     if r1.get("status") == "success" and r1.get("data", {}).get("candles"):
#         candles = r1["data"]["candles"]
#         if len(candles) != 0:
#             return candles[0][2], candles[0][3]
#     return "", ""

# def monthwise(id):
#     previous_date1 = current_date - relativedelta(months=1)
#     previous_date = previous_date1.strftime('%Y-%m-%d')
#     url = f"https://api.upstox.com/v2/historical-candle/{id}/month/{current_date}/{previous_date}"
#     headers = {'Accept': 'application/json'}
#     payload = {}
#     response = requests.request("GET", url, headers=headers, data=payload)
#     r1 = json.loads(response.text)
#     if r1.get("status") == "success" and r1.get("data", {}).get("candles"):
#         candles = r1["data"]["candles"]
#         if len(candles) != 0:
#             return candles[0][2], candles[0][3]
#     return "", ""
# # data = pd.read_csv("stocks_raw.csv",index_col=0)
# # for i in range(data.shape[0]):
    
# #     x1 = str(data.at[i,'instrument_key'])
# #     x,y=monthwise(x1)
# #     a,b=weekly(x1)
# #     m,n=daywise(x1)
# #     # e,f=minutewise(x1)
# #     data.at[i,'month_high']=x
# #     data.at[i,'month_low']=y
# #     data.at[i,'week_high']=a
# #     data.at[i,'week_low']=b
# #     data.at[i,'day_high']=m
# #     data.at[i,'day_low']=n
# #     # data.at[i,'minute_high']=e
# #     # data.at[i,'minute_low']=f
# #     data.to_csv("updated.csv")

# def update_vector_store():
#     embed = OpenAIEmbeddings(openai_api_key="sk-proj-sFmN2dibkkuuUxxrAeDPT3BlbkFJhY7iwpaB5jZLJYDWoB1C")
#     vector_store_path = "admin"

#     data = pd.read_csv("stocks_raw.csv", index_col=0, nrows=10)
#     texts = []

#     # Read the list of processed stocks from the file
#     try:
#         with open("processed_stocks.txt", "r") as file:
#             processed_stocks = file.read().splitlines()
#     except FileNotFoundError:
#         processed_stocks = []

#     for i in range(data.shape[0]):
#         x1 = str(data.at[i, 'instrument_key'])

#         # Check if the stock has already been processed
#         if x1 in processed_stocks:
#             continue

#         x, y = monthwise(x1)
#         a, b = weekly(x1)
#         m, n = daywise(x1)

#         # Handle empty strings and convert to NaN
#         x = float('nan') if x == '' else x
#         y = float('nan') if y == '' else y
#         a = float('nan') if a == '' else a
#         b = float('nan') if b == '' else b
#         m = float('nan') if m == '' else m
#         n = float('nan') if n == '' else n

#         data.at[i, 'month_high'] = x
#         data.at[i, 'month_low'] = y
#         data.at[i, 'week_high'] = a
#         data.at[i, 'week_low'] = b
#         data.at[i, 'day_high'] = m
#         data.at[i, 'day_low'] = n

#         stock_text = f"{data.at[i, 'name']} - Month High: {x}, Month Low: {y}, Week High: {a}, Week Low: {b}, Day High: {m}, Day Low: {n}"
#         texts.append(stock_text)

#         # Add the stock to the processed list
#         processed_stocks.append(x1)

#     data1 = data.drop(columns=['instrument_key'])
#     data1.to_csv("updated.csv", index=False)
#     print(texts)

#     # Write the updated list of processed stocks to the file
#     with open("processed_stocks.txt", "w") as file:
#         file.write("\n".join(processed_stocks))

#     if not os.path.exists(vector_store_path):
#         loader = CSVLoader(file_path='updated.csv', encoding='utf-8')
#         documents = loader.load()
#         vectors0 = FAISS.from_documents(documents, embed)
#         vectors0.save_local("admin")
#         print("embeding done")
#         logging.info("New vector store created with updated stock data.")
#     else:
#         vector_store = FAISS.load_local(vector_store_path, embeddings=embed, allow_dangerous_deserialization=True)
#         vector_store.add_texts(texts, embeddings=embed.embed_documents(texts))
#         vector_store.save_local(vector_store_path)
#         print("embeding done")
#         logging.info("Existing vector store updated with new stock data.")

# if __name__ == "__main__":
#     update_vector_store()

import requests
import pandas as pd
import json
import time
from langchain.document_loaders import CSVLoader
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

current_date = datetime.now().date()

def minutewise(id):
    previous_date1 = current_date - timedelta(days=1)
    previous_date = previous_date1.strftime('%Y-%m-%d')
    url = f"https://api.upstox.com/v2/historical-candle/{id}/1minute/{current_date}"
    headers = {'Accept': 'application/json'}
    payload = {}
    logging.info(f"Requesting 1-minute data from URL: {url}")
    response = requests.request("GET", url, headers=headers, data=payload)
    r1 = json.loads(response.text)
    if r1.get("status") == "success" and r1.get("data", {}).get("candles"):
        candles = r1["data"]["candles"]
        if len(candles) != 0:
            return candles[0][2], candles[0][3]
    return "", ""

def daywise(id):
    current_date1 = current_date - timedelta(days=1)
    current_date2 = current_date1.strftime('%Y-%m-%d')
    previous_date1 = current_date1 - timedelta(days=2)
    previous_date = previous_date1.strftime('%Y-%m-%d')
    url = f"https://api.upstox.com/v2/historical-candle/{id}/day/{current_date2}/{previous_date}"
    headers = {'Accept': 'application/json'}
    payload = {}
    logging.info(f"Requesting day-wise data from URL: {url}")
    response = requests.request("GET", url, headers=headers, data=payload)
    r1 = json.loads(response.text)
    if r1.get("status") == "success" and r1.get("data", {}).get("candles"):
        candles = r1["data"]["candles"]
        if len(candles) != 0:
            return candles[0][2], candles[0][3]
    return "", ""

def weekly(id):
    previous_date1 = current_date - timedelta(days=7)
    previous_date = previous_date1.strftime('%Y-%m-%d')
    url = f"https://api.upstox.com/v2/historical-candle/{id}/week/{current_date}/{previous_date}"
    headers = {'Accept': 'application/json'}
    payload = {}
    logging.info(f"Requesting weekly data from URL: {url}")
    response = requests.request("GET", url, headers=headers, data=payload)
    r1 = json.loads(response.text)
    if r1.get("status") == "success" and r1.get("data", {}).get("candles"):
        candles = r1["data"]["candles"]
        if len(candles) != 0:
            return candles[0][2], candles[0][3]
    return "", ""

def monthwise(id):
    previous_date1 = current_date - relativedelta(months=1)
    previous_date = previous_date1.strftime('%Y-%m-%d')
    url = f"https://api.upstox.com/v2/historical-candle/{id}/month/{current_date}/{previous_date}"
    headers = {'Accept': 'application/json'}
    payload = {}
    logging.info(f"Requesting monthly data from URL: {url}")
    response = requests.request("GET", url, headers=headers, data=payload)
    r1 = json.loads(response.text)
    if r1.get("status") == "success" and r1.get("data", {}).get("candles"):
        candles = r1["data"]["candles"]
        if len(candles) != 0:
            return candles[0][2], candles[0][3]
    return "", ""

def update_vector_store():
    embed = OpenAIEmbeddings(openai_api_key="sk-proj-sFmN2dibkkuuUxxrAeDPT3BlbkFJhY7iwpaB5jZLJYDWoB1C")
    vector_store_path = "admin"

    data = pd.read_csv("stocks_raw.csv", index_col=0, nrows=10)
    texts = []

    # Read the list of processed stocks from the file
    try:
        with open("processed_stocks.txt", "r") as file:
            processed_stocks = file.read().splitlines()
    except FileNotFoundError:
        processed_stocks = []

    for i in range(data.shape[0]):
        x1 = str(data.at[i, 'instrument_key'])

        # Check if the stock has already been processed
        if x1 in processed_stocks:
            continue

        x, y = monthwise(x1)
        a, b = weekly(x1)
        m, n = daywise(x1)

        # Handle empty strings and convert to NaN
        x = float('nan') if x == '' else x
        y = float('nan') if y == '' else y
        a = float('nan') if a == '' else a
        b = float('nan') if b == '' else b
        m = float('nan') if m == '' else m
        n = float('nan') if n == '' else n

        data.at[i, 'month_high'] = x
        data.at[i, 'month_low'] = y
        data.at[i, 'week_high'] = a
        data.at[i, 'week_low'] = b
        data.at[i, 'day_high'] = m
        data.at[i, 'day_low'] = n

        stock_text = f"{data.at[i, 'name']} - Month High: {x}, Month Low: {y}, Week High: {a}, Week Low: {b}, Day High: {m}, Day Low: {n}"
        texts.append(stock_text)

        # Add the stock to the processed list
        processed_stocks.append(x1)

    data1 = data.drop(columns=['instrument_key'])
    data1.to_csv("updated.csv", index=False)
    logging.info("Updated stock data: %s", texts)

    # Write the updated list of processed stocks to the file
    with open("processed_stocks.txt", "w") as file:
        file.write("\n".join(processed_stocks))

    if not os.path.exists(vector_store_path):
        loader = CSVLoader(file_path='updated.csv', encoding='utf-8')
        documents = loader.load()
        vectors0 = FAISS.from_documents(documents, embed)
        vectors0.save_local("admin")
        logging.info("New vector store created with updated stock data.")
    else:
        vector_store = FAISS.load_local(vector_store_path, embeddings=embed, allow_dangerous_deserialization=True)
        vector_store.add_texts(texts, embeddings=embed.embed_documents(texts))
        vector_store.save_local(vector_store_path)
        logging.info("Existing vector store updated with new stock data.")

if __name__ == "__main__":
    update_vector_store()
