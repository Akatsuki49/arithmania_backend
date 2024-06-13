import requests
import pandas as pd
import json
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
import logging

current_date = datetime.now().date()
# access_token="eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI1UUFNOFAiLCJqdGkiOiI2NjFiMWMzODc5ZTMxZTNjNmNlMmQ4NjciLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaXNBY3RpdmUiOnRydWUsInNjb3BlIjpbImludGVyYWN0aXZlIiwiaGlzdG9yaWNhbCJdLCJpYXQiOjE3MTMwNTI3MjgsImlzcyI6InVkYXBpLWdhdGV3YXktc2VydmljZSIsImV4cCI6MTcxMzEzMjAwMH0.0uWuMeegluQvYvkf-u3WEgFj30Zm0p_X510Hiuk9JPY"

def minutewise(id):
    previous_date1 = current_date - timedelta(days=1)
    previous_date = previous_date1.strftime('%Y-%m-%d')
    url = f"https://api.upstox.com/v2/historical-candle/{id}/1minute/{current_date}"
    headers = {'Accept': 'application/json'}
    payload = {}
    print(url)
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
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
    print(url)
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
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
    print(url)
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
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
    response = requests.request("GET", url, headers=headers, data=payload)
    r1 = json.loads(response.text)
    if r1.get("status") == "success" and r1.get("data", {}).get("candles"):
        candles = r1["data"]["candles"]
        if len(candles) != 0:
            return candles[0][2], candles[0][3]
    return "", ""
# data = pd.read_csv("stocks_raw.csv",index_col=0)
# for i in range(data.shape[0]):
    
#     x1 = str(data.at[i,'instrument_key'])
#     x,y=monthwise(x1)
#     a,b=weekly(x1)
#     m,n=daywise(x1)
#     # e,f=minutewise(x1)
#     data.at[i,'month_high']=x
#     data.at[i,'month_low']=y
#     data.at[i,'week_high']=a
#     data.at[i,'week_low']=b
#     data.at[i,'day_high']=m
#     data.at[i,'day_low']=n
#     # data.at[i,'minute_high']=e
#     # data.at[i,'minute_low']=f
#     data.to_csv("updated.csv")

def update_vector_store():
    API_KEY = "sk-proj-sFmN2dibkkuuUxxrAeDPT3BlbkFJhY7iwpaB5jZLJYDWoB1C"
    embed = OpenAIEmbeddings(openai_api_key=API_KEY)
    vector_store_path = "admin"

    data = pd.read_csv("stocks_raw.csv", index_col=0)
    texts = []

    # Read the list of processed stocks from the file
    try:
        with open("processed_stocks.txt", "r") as file:
            processed_stocks = file.read().splitlines()
    except FileNotFoundError:
        processed_stocks = []

    for i in range(200):
        

        x1 = str(data.at[i, 'instrument_key'])

        # Check if the stock has already been processed
        if x1 in processed_stocks:
            continue

        x, y = monthwise(x1)
        a, b = weekly(x1)
        m, n = daywise(x1)

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

    data.to_csv("updated.csv", index=False)

    # Write the updated list of processed stocks to the file
    with open("processed_stocks.txt", "w") as file:
        file.write("\n".join(processed_stocks))

    if not os.path.exists(vector_store_path):
        vector_store = FAISS.from_texts(texts=texts, embedding=embed)
        vector_store.save_local(vector_store_path)
        logging.info("New vector store created with updated stock data.")
    else:
        vector_store = FAISS.load_local(vector_store_path, embeddings=embed, allow_dangerous_deserialization=True)
        vector_store.add_texts(texts)
        vector_store.save_local(vector_store_path)
        logging.info("Existing vector store updated with new stock data.")
