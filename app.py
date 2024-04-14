from flask import Flask, request, jsonify, url_for, redirect
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from openai import OpenAI
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS


app = Flask(__name__)

# Replace with your actual API key
API_KEY = "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"
embed = OpenAIEmbeddings(openai_api_key=API_KEY)

# Folder name to store FAISS index
folder_name = "store"

text_splitter = CharacterTextSplitter(
    chunk_size = 512,
    chunk_overlap  = 24,
    length_function = len,
    separator="\n"
)

chunks = text_splitter.split_text("Introduction to Finance")


# Initialize the vector store path
vector_store_path = os.path.join(folder_name, "vector_store.faiss")


# Check if the vector store exists
if not os.path.exists(vector_store_path):
    # Initialize the vector store if it doesn't exist
    vector_store = FAISS.from_texts(texts=chunks, embedding=embed)

    # Save the vector store
    vector_store.save_local(vector_store_path)
else:
    # Load the vector store if it exists
    vector_store = FAISS.load_local(vector_store_path, embeddings=embed, allow_dangerous_deserialization=True)
@app.route('/update_transactions', methods=['POST'])
def update_transactions():
    try:
        # Get transaction details from the request form data
        user_id = request.form.get('user_id')
        if user_id is None:
            return jsonify({'error': 'user_id is required'}), 400

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

        # Construct transaction text
        transaction_text = f"{amount} {transaction_type} {category} {description}"

        # Generate embedding for the transaction text
        embedding = embed.embed_query(transaction_text)

        # Update the vector store with the new embedding
        vector_store.add_texts([transaction_text], embeddings=[embedding])

        # Save the updated vector store
        vector_store.save_local(vector_store_path)

        return jsonify({'message': 'Transaction embeddings updated successfully'})

    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500
@app.route('/query', methods=['POST'])
def query():

    question = request.form['question']
    user_id = request.form['user_id']
    classification = "financial education"  # classify_question(question)
    if classification == "investment":
        return redirect(url_for('investments', question=question, user_id=user_id))
    elif classification == "personal budgeting":
        return redirect(url_for('personal_budgeting', question=question, user_id=user_id))
    elif classification == "financial education":
        return redirect(url_for('financial_education', question=question, user_id=user_id))
    else:
        return jsonify({'error': 'Invalid classification'})
@app.route('/investments')
def investments():
    question = request.args.get('question', '')
    return jsonify({'question': question, 'message': 'Investments route'})


@app.route('/personal_budgeting', methods=['POST'])
def personal_budgeting():
    question = request.form.get('question')
    user_id = request.form.get('user_id')

    if not question or not user_id:
        return jsonify({'error': 'question and user_id are required'}), 400

    try:
        # Call the query_llm function
        response = query_llm(vector_store_path, question)
        return jsonify({'question': question, 'message': response, 'user_id': user_id})

    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

def query_llm(cid, quest):
    embed1 = OpenAIEmbeddings(openai_api_key=API_KEY)
    vs = FAISS.load_local(str(cid), embeddings=embed1, allow_dangerous_deserialization=True)
    llm = ChatOpenAI(openai_api_key=API_KEY)
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vs.as_retriever(),
        memory=memory
    )
    result = conversation_chain({"question": str(quest)})['answer']
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
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
