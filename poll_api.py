import requests
import pandas as pd
import json
import time
import shutil
from astrapy.constants import VectorMetric
from langchain.document_loaders import TextLoader
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.embeddings import OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS
import os
from langchain_astradb import AstraDBVectorStore
from langchain_core.documents import Document
from astrapy import DataAPIClient
from langchain.text_splitter import CharacterTextSplitter
import logging
from langchain_community.embeddings import HuggingFaceEmbeddings
 
ASTRA_DB_APPLICATION_TOKEN = "AstraCS:WpfykZJsLDoLlKhPPSiUwXAZ:13a5785189fda1003cc43d7056ef67d4c09d6cd82fed033f8205b8745e5f6eaa"
ASTRA_DB_API_ENDPOINT = "https://751276ca-4055-41e2-8319-3be1085320fc-us-east1.apps.astra.datastax.com"  # Replace with your actual endpoint
# ASTRA_DB_KEYSPACE = "default_keyspace"
collection_name="rai"
embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)



    

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

    curdir = os.path.dirname(os.path.abspath(__file__))
    fp = os.path.join(curdir,"processed_stocks.txt")
    if os.path.exists(fp):
        os.remove(fp)
    client = DataAPIClient(ASTRA_DB_APPLICATION_TOKEN)
    database = client.get_database(ASTRA_DB_API_ENDPOINT)
    x = database.list_collection_names()
    if "rai" in x:
        database.drop_collection("rai")
    # collection = database.get_collection("rai1")



    def split_text_to_line_chunks(text, lines_per_chunk=10):
        """ Split text into chunks of every lines_per_chunk lines. """
        lines = text.splitlines()
        chunks = []
        for i in range(0, len(lines), lines_per_chunk):
            chunk = "\n".join(lines[i:i + lines_per_chunk])
            chunks.append(chunk)
        return chunks


    data = pd.read_csv("stocks_raw.csv", index_col=0)
    texts = []
    z1=[]

    # Read the list of processed stocks from the file
    # try:
    #     with open("processed_stocks.txt", "r", encoding='utf-8') as file:
    #         processed_stocks = file.read()

    # except FileNotFoundError:
    #     processed_stocks = []

    for i in range(data.shape[0]):
        
        x1 = str(data.at[i, 'instrument_key'])

        # Check if the stock has already been processed
        # if x1 in processed_stocks:
        #     continue

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
        # if(i==0):
        #     vectors0 = FAISS.from_texts(texts = texts,embedding = embed)
        #     vectors0.save_local("admin")
        #     texts=[]
        # elif(i%3==0 and i>0):
        #     vectors1= FAISS.load_local(vector_store_path, embeddings=embed, allow_dangerous_deserialization=True)
        #     vectors1.add_texts(texts=texts)
        #     shutil.rmtree("admin")
        #     vectors1.save_local("admin")
        #     texts=[]
        # Add the stock to the processed list
        # processed_stocks.append(x1)

    # data.drop(columns=['instrument_key']).to_csv("updated.csv", index=False)
    # print(texts)

    # Write the updated list of processed stocks to the file
    with open("processed_stocks.txt", "w", encoding='utf-8') as file:
        for stock in texts:
            file.write(stock+"\n")
    with open("processed_stocks.txt", "r", encoding='utf-8') as file:
        processed_stocks = file.read()
    collection = database.create_collection(collection_name,dimension=384,metric=VectorMetric.COSINE)

    vstore = AstraDBVectorStore(
    embedding=embeddings,
    collection_name=collection_name,
    token=ASTRA_DB_APPLICATION_TOKEN,
    api_endpoint=ASTRA_DB_API_ENDPOINT,
    )
    text_splitter = CharacterTextSplitter(
        chunk_size=256,  # Initial chunk size
        chunk_overlap=100,  # Overlap to ensure context continuity
        length_function=len,
        separator="\n"
        )
    initial_chunks = text_splitter.split_text(processed_stocks)

    # Further split each chunk to ensure it's within the 10 lines per chunk
    final_chunks = []
    for chunk in initial_chunks:
        final_chunks.extend(split_text_to_line_chunks(chunk, lines_per_chunk=10))
    
    docs = [Document(page_content=chunk) for chunk in final_chunks]
    sample_embedding = embeddings.embed_documents([docs[0].page_content])[0]
    vstore.add_documents(docs)


    # embedding_dim = len(sample_embedding)
    # if not os.path.exists(vector_store_path):
    #     loader = TextLoader('processed_stocks.txt')
    #     documents = loader.load()
    #     ts = RecursiveCharacterTextSplitter(chunk_size=100,chunk_overlap=50)
    #     docs = ts.split_documents(documents)
    #     vectors0 = FAISS.from_documents(docs, embed)
    #     vectors0.save_local("admin")
    #     print(vectors0.index.ntotal)
    #     logging.info("New vector store created with updated stock data.")
    # else:
    #     vector_store = FAISS.load_local(vector_store_path, embeddings=embed, allow_dangerous_deserialization=True)
    #     # vector_store.add_texts(texts)
    #     vector_store.save_local(vector_store_path)
    #     logging.info("Existing vector store updated with new stock data.")


update_vector_store()
# client = DataAPIClient(ASTRA_DB_APPLICATION_TOKEN)
# database = client.get_database(ASTRA_DB_API_ENDPOINT)
# x = database.list_collection_names()
# print(x)
# if "rai" in x:
#     database.drop_collection("rai")