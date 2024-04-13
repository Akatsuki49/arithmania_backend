from flask import Flask, request

app = Flask(__name__)


@app.route('/ask_question', methods=['POST'])
def ask_question():
    question = request.form['question']
    answer = '42'
    return jsonify({'answer': answer})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
