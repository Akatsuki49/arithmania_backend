from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain_community.chat_models import OpenAI
from langchain_openai import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.csv_loader import CSVLoader
import warnings
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_community.vectorstores import FAISS
warnings.filterwarnings("ignore")

def answgen(question1):
    OPENAI_API_KEY="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"
    embedd = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectors = FAISS.load_local("admin",embedd,allow_dangerous_deserialization=True)
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(llm = OpenAI(openai_api_key="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",temperature=0.0),retriever=vectors.as_retriever(),memory=memory)
    question = f'{question1} given the question, answer it based on the database provided and analyze that database and give answer. You can also add on information if you feel something is missing in the database'
    result = conversation_chain({"question":str(question)})['answer']
    return result

