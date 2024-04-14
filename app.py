from flask import Flask, request, jsonify, url_for, redirect
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from openai import OpenAI
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import requests
# from model_load import classify_question

app = Flask(__name__)

# Replace with your actual API key
API_KEY = "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"
embed = OpenAIEmbeddings(openai_api_key=API_KEY)

folder_name = "store"


@app.route('/update_transactions', methods=['POST'])
def update_transactions():
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
        embedding = embed.embed_query(transaction_text)

        if not os.path.exists(vector_store_path):
            vector_store = FAISS.from_texts(
                texts=[transaction_text], embedding=embed)
            vector_store.save_local(vector_store_path)
        else:
            print("here")
            vector_store = FAISS.load_local(
                vector_store_path, embeddings=embed, allow_dangerous_deserialization=True)
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

        # Prepare the data to be sent in the request body
        data = {
            'user_id': user_id,
            'question': question
        }

        # Make a POST request to the desired endpoint based on classification
        classification = "personal budgeting"
        if classification == "investment":
            response = requests.post(
                'https://e9ac-104-28-220-172.ngrok-free.app/investments', data=data)
        elif classification == "personal budgeting":
            response = requests.post(
                'https://e9ac-104-28-220-172.ngrok-free.app/personal_budgeting', data=data)
        elif classification == "financial education":
            response = requests.post(
                'https://e9ac-104-28-220-172.ngrok-free.app/financial_education', data=data)
        else:
            return jsonify({'error': 'Invalid classification'})

        # Process the response as needed
        if response.status_code == 200:
            return jsonify({'message': 'Transaction added successfully'}), 200
        else:
            return jsonify({'error': 'Failed to add transaction'}), 500

    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500


@app.route('/investments')
def investments():
    question = request.args.get('question', '')
    return jsonify({'question': question, 'message': 'Investments route'})


@app.route('/personal_budgeting', methods=['POST'])
def personal_budgeting():
    try:
        user_id = request.form.get('user_id')
        question = request.form.get('question')
        if not question or not user_id:
            return jsonify({'error': 'question and user_id are required'}), 400

        user_folder = os.path.join(folder_name, user_id)
        vector_store_path = user_folder

        result = query_llm(vector_store_path, question)
        return jsonify({'question': question, 'message': result, 'user_id': user_id})

    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500


def query_llm(vector_store_path, question):
    print(vector_store_path)
    embed1 = OpenAIEmbeddings(openai_api_key=API_KEY)
    vs = FAISS.load_local(str(vector_store_path),
                          embeddings=embed1, allow_dangerous_deserialization=True)
    llm = ChatOpenAI(openai_api_key=API_KEY)
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vs.as_retriever(),
        memory=memory
    )
    result = conversation_chain({"question": str(question)})['answer']
    return result


@app.route('/financial_education')
def financial_education():
    question = request.args.get('question', '')

    try:
        prompt = f"Given this message explain in a simple and understandable way: {question}"

        client = OpenAI(api_key=API_KEY)
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=140,
            model="gpt-3.5-turbo",
            temperature=0.7,
        )

        if response and response.choices:
            generated_text = response.choices[0].message.content
            return jsonify({'question': question, 'message': generated_text})
        else:
            return jsonify({'error': 'No response from the model'}), 500

    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
