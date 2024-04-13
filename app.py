from flask import Flask, request, jsonify, redirect
from model_load import classify_question

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    question = request.form['question']
    # Use the middleware to classify the question
    classification = classify_question(question)
    # Redirect to the appropriate route based on classification
    if classification == "investment":
        return redirect('/investments')
    elif classification == "personal budgeting":
        return redirect('/personal_budgeting')
    elif classification == "financial education":
        return redirect('/financial_education')
    else:
        return jsonify({'error': 'Invalid classification'})

@app.route('/investments')
def investments():
    # Implement your logic for investments route here
    return jsonify({'message': 'Investments route'})

@app.route('/personal_budgeting')
def personal_budgeting():
    # Implement your logic for personal budgeting route here
    return jsonify({'message': 'Personal Budgeting route'})

@app.route('/financial_education')
def financial_education():
    # Implement your logic for financial education route here
    return jsonify({'message': 'Financial Education route'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
