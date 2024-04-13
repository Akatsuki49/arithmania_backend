from flask import Flask, request, jsonify, redirect, url_for
#from model_load import classify_question

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    question = request.form['question']
    # Use the middleware to classify the question
    classification = "personal budgeting" #classify_question(question)
    # Redirect to the appropriate route based on classification
    if classification == "investment":
        return redirect(url_for('investments', question=question))
    elif classification == "personal budgeting":
        return redirect(url_for('personal_budgeting', question=question))
    elif classification == "financial education":
        return redirect(url_for('financial_education', question=question))
    else:
        return jsonify({'error': 'Invalid classification'})

@app.route('/investments')
def investments():
    # Retrieve question from URL query parameters
    question = request.args.get('question', '')
    # Implement your logic for investments route here

    return jsonify({'question': question, 'message': 'Investments route'})

@app.route('/personal_budgeting')
def personal_budgeting():
    # Retrieve question from URL query parameters
    question = request.args.get('question', '')
    # Implement your logic for personal budgeting route here
    return jsonify({'question': question, 'message': 'Personal Budgeting route'})

@app.route('/financial_education')
def financial_education():
    # Retrieve question from URL query parameters
    question = request.args.get('question', '')
    # Implement your logic for financial education route here
    return jsonify({'question': question, 'message': 'Financial Education route'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
