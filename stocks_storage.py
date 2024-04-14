from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import FAISS
import pandas as pd


loader0 = CSVLoader(file_path='updated.csv', encoding="utf-8")
data0 = loader0.load()
embeddings = OpenAIEmbeddings(openai_api_key="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")
vectors0 = FAISS.from_documents(data0, embeddings)
vectors0.save_local("admin")
