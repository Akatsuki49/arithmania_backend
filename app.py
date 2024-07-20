from flask import Flask, request, jsonify
# from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from openai import OpenAI
from langchain_astradb import AstraDBVectorStore
from groq import Groq
import os
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_experimental.agents.agent_toolkits import create_csv_agent
# from langchain.agents.agent_types import AgentType
# from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import subprocess
import time
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import boto3


# from model_load import classify_question

app = Flask(__name__)
# API_KEY = "sk-proj-sFmN2dibkkuuUxxrAeDPT3BlbkFJhY7iwpaB5jZLJYDWoB1C"


# llm=ChatOpenAI(temperature=0.1,openai_api_key = API_KEY)

# agent = create_csv_agent(
#     llm,
#     "updated.csv",
#     verbose=True,
#     agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     allow_dangerous_code=True,
#     handle_parsing_errors=True
# )

# # Replace with your actual API key
# embed = OpenAIEmbeddings(openai_api_key=API_KEY)

ASTRA_DB_APPLICATION_TOKEN = "AstraCS:WpfykZJsLDoLlKhPPSiUwXAZ:13a5785189fda1003cc43d7056ef67d4c09d6cd82fed033f8205b8745e5f6eaa"
ASTRA_DB_API_ENDPOINT = "https://751276ca-4055-41e2-8319-3be1085320fc-us-east1.apps.astra.datastax.com"  # Replace with your actual endpoint
# ASTRA_DB_KEYSPACE = "default_keyspace"
collection_name="rai"
# embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
# embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)



folder_name = "store"
stock_folder_name = "processed_stocks.txt"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def update_stock_data():
    try:
        subprocess.run(["python", "poll_api.py"])
        logging.info("Stock data updated successfully.")
    except Exception as e:
        logging.error(f"Error updating stock data: {str(e)}")



@app.route('/update_transactions', methods=['POST'])
def update_transactions():
    
    embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
    try:
        user_id = request.form.get('user_id')
        if user_id is None:
            return jsonify({'error': 'user_id is required'}), 400

        user_folder = os.path.join(folder_name, user_id)
        # os.makedirs(user_folder, exist_ok=True)
        vector_store_path = os.path.join(user_folder)
        print(vector_store_path)

        amount = request.form.get('amount')
        if amount is None:
            return jsonify({'error': 'amount is required'}), 400

        transaction_type = request.form.get('type')
        if transaction_type is None:
            return jsonify({'error': 'type is required'}), 400

        category = request.form.get('category')
        if category is None:
            return jsonify({'error': 'category is required'}), 400

        description = request.form.get('description')
        if description is None:
            return jsonify({'error': 'description is required'}), 400

        transaction_text = f"{amount} {transaction_type} {category} {description}"
        embedding = embeddings.embed_query(transaction_text)

        if not os.path.exists(vector_store_path):
            vector_store = FAISS.from_texts(
                texts=[transaction_text], embedding=embeddings)
            vector_store.save_local(vector_store_path)
        else:
            print("here")
            vector_store = FAISS.load_local(
                vector_store_path, embeddings=embeddings, allow_dangerous_deserialization=True)
            vector_store.add_texts([transaction_text], embeddings=[embedding])
            vector_store.save_local(vector_store_path)

        return jsonify({'message': 'Transaction embeddings updated successfully'})

    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500


@app.route('/query', methods=['POST'])
def query():
    try:
        user_id = request.form.get('user_id')
        if user_id is None:
            return jsonify({'error': 'user_id is required'}), 400

        question = request.form.get('question')
        if question is None:
            return jsonify({'error': 'question is required'}), 400
        # classification = classify_question(question)
        classification = "financial education"
        # classification = "personal budgeting"
        # classification = "financial education"
        # Make a POST request to the desired endpoint based on classification
        # classification = "personal budgeting"
        if classification == "stock market":
            response = invest(user_id, question)
        elif classification == "personal budgeting":
            response = personal_budgeting(user_id, question)
        elif classification == "financial education":
            response = financial_education(user_id, question)
        else:
            return jsonify({'error': 'Invalid classification'})

        # Process the response as needed
        # print(response)
        if response['status_code'] == 200:
            return jsonify({'message': 'Successful', 'response': response['message']}), 200
        else:
            return jsonify({'error': 'Failure'}), 500

    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500


# @app.route('/investments')
# def invest(user_id, question):
#     answer1 = answgen(question)
#     return {'question': question, 'message': answer1, 'status_code': 200}

def invest(user_id, question):
    try:
        embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
        embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
        vstore = AstraDBVectorStore(
        embedding=embeddings,
        collection_name=collection_name,
        token=ASTRA_DB_APPLICATION_TOKEN,
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        )
        vector_store_path = stock_folder_name
        last_update_time = os.path.getmtime(vector_store_path)
        current_time = time.time()
        time_since_last_update = current_time - last_update_time

        # if time_since_last_update > 30:  # Update if it's been more than 30 seconds
        #     update_stock_data()
        #     logging.info("Stock data updated before serving the request.")

        # result = query_llm(vector_store_path, question)
        result = vstore.similarity_search(str(question),k=1)
        for res in result:
            x1 = res.page_content
        client = Groq(
            api_key="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",
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{x1}+\n\n\n+{question}+\n\n\n+Give a short and precise answer no more than 100 words in one paragraph.",
                }
            ],
            model="llama3-70b-8192",
        )

        res1 = chat_completion.choices[0].message.content
        return {'question': question, 'message': res1, 'status_code': 200}
    except Exception as e:
        logging.error(f"Error occurred in invest function: {str(e)}")
        return {'error': f"An error occurred: {str(e)}", 'status_code': 500}

# @app.route('/personal_budgeting', methods=['POST'])
def personal_budgeting(user_id, question):
    try:
        if not question or not user_id:
            return {'error': 'question and user_id are required', 'status_code': 200}

        user_folder = os.path.join(folder_name, user_id)
        vector_store_path = user_folder

        result = query_llm(vector_store_path, question)
        return {'question': question, 'message': result, 'user_id': user_id, 'status_code': 200}

    except Exception as e:
        return {'error': f"An error occurred: {str(e)}", 'status_code': 500}


def query_llm(vector_store_path, question):
    print(vector_store_path)
    embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
    # embed1 = OpenAIEmbeddings(openai_api_key=API_KEY)
    vs = FAISS.load_local(str(vector_store_path),
                          embeddings=embeddings, allow_dangerous_deserialization=True)
    # llm = ChatOpenAI(openai_api_key=API_KEY,temperature=0.1)
    llm = ChatGroq(groq_api_key = "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", model_name = "llama3-70b-8192")
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vs.as_retriever(),
        memory=memory
    )
    result = conversation_chain({"question": str(question)})['answer']
    return result


# @app.route('/financial_education')
def financial_education(user_id, question):
    try:
        # prompt = f""

        client = Groq(
            api_key="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",
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Assume that you are a Financial Advisor in India. Given this message explain in a simple and understandable way not more than 100 words:+\n\n+{question}",
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0.1
        )


        # if chat_completion and chat_completion.choices:
        res12 = chat_completion.choices[0].message.content
        return {'question': question, 'message': res12, 'status_code': 200}
        # else:
            # return {'error': 'No response from the model', 'status_code': 500}

    except Exception as e:
        return {'error': f"An error occurred: {str(e)}", 'status_code': 500}

# def init_scheduler():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(update_stock_data, 'interval', seconds=10)
#     scheduler.start()

if __name__ == '__main__':
    # init_scheduler()
    app.run(host='0.0.0.0', port=8080, debug=True)
