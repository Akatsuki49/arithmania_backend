# R.AI

## Problem Statement

Managing personal finances can be overwhelming and confusing, especially with the multitude of expenses and investment options available. Many individuals struggle to create effective budgets, track their spending, and make informed decisions about their financial future. Furthermore, keeping up with the latest stock market information and financial advice can be time-consuming and complex.

## Proposed Solution

Our app offers a comprehensive and easy-to-use financial advisor tool that helps users manage their finances efficiently. Key features include:

### 1. Budgeting Assistance
Get detailed information about your expenses and personalized advice on how to reduce them.

### 2. Financial Guidance
Access general financial advice on a wide range of topics to help you make informed decisions.

### 3. Stock Market Updates
Stay up-to-date with the latest stock information, regularly updated to reflect current market conditions.

## How to Run

First you need to start a CORS server (We have used ngrok for that)

Open Command Prompt and run

```bash
ngrok http --host-header=rewrite 5000
```

Install the requirements needed to run the server using 

```bash
pip install -r requirements.txt
```

Run the backend using

```bash
python app.py
```

Don't forget to add your own `.env` with **GROQ_API_KEY**

If the `app.py` runs fine, you should be able to see `Running on http://127.0.0.1:8080` in the terminal.

## Output

## Summary of Main Novelties

- **Full Stack Project:** We've developed a comprehensive solution comprising frontend (Flutter, Dart, Figma) and backend (Python, Flask, Firebase, Llama3, FAISS, VectorDB), along with a proxy server (ngrok).

- **Regular Updates:** There will be regular updates on the stock market data using repeated API calls and polling techniques. 

- **Classification Process:** Utilizing **Llama3**, we classify the question provided by the user whether it is related to stock market, personal budgeting or general financial education.

- **Prompt Engineered Output:** Our final output is engineered based on the input prompt provided to the interface.

- **VectorDB Store:** We used a third-party application AstraDB as a vector store for storing chunks of data and similarity search to fetch data based on cosine similarity of the query and the chunk. We also used FAISS Vector Indexing to store data locally for personal budgeting, so that the user data is not exposed.

- **Hassle-Free UI:** The design is handpicked to make the user experience as smooth as possible. You can login using your google account as well as create your own account using your email ID.

## App Screens
### Welcome Screen
<img src="https://github.com/user-attachments/assets/428aa1f5-ff57-4353-b0cf-c01689cebc9e" alt="Welcome Screen" width="300">


### Login Page
<img src="https://github.com/user-attachments/assets/b30f38f6-bb71-43e4-9ddf-5e0ef6e50b8b" alt="Login Page" width="300">


### Select Mode of Chart (Audio/Text)
<img src="https://github.com/user-attachments/assets/7e2ce03c-4a8e-4373-a468-e2015ba2270d" alt="Select Mode of Chart" width="300">

### Chat Screen with Output Example

<img src="https://github.com/user-attachments/assets/f36b706c-d487-4763-a20c-fd6220616528" alt="Chat Screen" width="300">

### Personal Budgeting Page

<img src="https://github.com/user-attachments/assets/e4b58070-ab73-43d0-be9a-aafe76b1c1f6" alt="Personal Budgeting Page" width="300">









