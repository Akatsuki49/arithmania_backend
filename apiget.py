import requests
import pandas as pd
import json
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

current_date = datetime.now().date()
# access_token="eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI1UUFNOFAiLCJqdGkiOiI2NjFiMWMzODc5ZTMxZTNjNmNlMmQ4NjciLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaXNBY3RpdmUiOnRydWUsInNjb3BlIjpbImludGVyYWN0aXZlIiwiaGlzdG9yaWNhbCJdLCJpYXQiOjE3MTMwNTI3MjgsImlzcyI6InVkYXBpLWdhdGV3YXktc2VydmljZSIsImV4cCI6MTcxMzEzMjAwMH0.0uWuMeegluQvYvkf-u3WEgFj30Zm0p_X510Hiuk9JPY"

def minutewise(id):
    previous_date1 = current_date - timedelta(days=1)
    previous_date = previous_date1.strftime('%Y-%m-%d')
    url = f"https://api.upstox.com/v2/historical-candle/{id}/1minute/{current_date}"
    headers = {
        'Accept': 'application/json'
    }
    payload = {}
    print(url)
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    r1 = json.loads(response.text)
    print(r1["data"]["candles"])
    if len(r1["data"]["candles"])!=0:
        return r1["data"]["candles"][0][2],r1["data"]["candles"][0][3]
    return "",""

def daywise(id):
    current_date1 = current_date - timedelta(days=1)
    current_date2 = current_date1.strftime('%Y-%m-%d')
    previous_date1 = current_date1 - timedelta(days=2)
    previous_date = previous_date1.strftime('%Y-%m-%d')
    url = f"https://api.upstox.com/v2/historical-candle/{id}/day/{current_date2}/{previous_date}"
    headers = {
        'Accept': 'application/json'
    }
    payload = {}
    print(url)
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    r1 = json.loads(response.text)
    print(r1["data"]["candles"])
    if len(r1["data"]["candles"])!=0:
        return r1["data"]["candles"][0][2],r1["data"]["candles"][0][3]
    return "",""

def weekly(id):
    previous_date1 = current_date - timedelta(days=7)
    previous_date = previous_date1.strftime('%Y-%m-%d')
    url = f"https://api.upstox.com/v2/historical-candle/{id}/week/{current_date}/{previous_date}"
    headers = {
        'Accept': 'application/json'
    }
    payload = {}
    print(url)
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    r1 = json.loads(response.text)
    print(r1["data"]["candles"])
    if len(r1["data"]["candles"])!=0:
        return r1["data"]["candles"][0][2],r1["data"]["candles"][0][3]
    return "",""

def monthwise(id):
    previous_date1 = current_date - relativedelta(months=1)
    previous_date = previous_date1.strftime('%Y-%m-%d')
    url = f"https://api.upstox.com/v2/historical-candle/{id}/month/{current_date}/{previous_date}"
    headers = {
        'Accept': 'application/json'
    }
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    r1 = json.loads(response.text)
    print(r1["data"]["candles"])
    if len(r1["data"]["candles"])!=0:
        return r1["data"]["candles"][0][2],r1["data"]["candles"][0][3]
    return "",""

data = pd.read_csv("stocks_raw.csv",index_col=0)
for i in range(data.shape[0]):
    if(i>0 and i%90==0):
        time.sleep(120)
    x1 = str(data.at[i,'instrument_key'])
    x,y=monthwise(x1)
    a,b=weekly(x1)
    m,n=daywise(x1)
    # e,f=minutewise(x1)
    data.at[i,'month_high']=x
    data.at[i,'month_low']=y
    data.at[i,'week_high']=a
    data.at[i,'week_low']=b
    data.at[i,'day_high']=m
    data.at[i,'day_low']=n
    # data.at[i,'minute_high']=e
    # data.at[i,'minute_low']=f
    data.to_csv("updated.csv")
