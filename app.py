from flask import Flask, request, jsonify, redirect, url_for
#from model_load import classify_question

from openai import OpenAI
import os
app = Flask(__name__)

API_KEY = "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"# Replace with your actual API key


@app.route('/query', methods=['POST'])
def query():
    question = request.form['question']
    classification = "financial education" #classify_question(question)
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

    try:
        # Prepare the prompt
        prompt = f"Given this message explain in a simple and understandable way: {question}"

        # Call the OpenAI API to generate a response
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
            # Extract the generated text from the response
            generated_text = response.choices[0].message.content

            # Return the generated text as a JSON response
            return jsonify({'question': question, 'message': generated_text})
        else:
            # Return an error message if there was no response from the model
            return jsonify({'error': 'No response from the model'}), 500

    except Exception as e:
        # Return an error message if there was an issue with the API call
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
