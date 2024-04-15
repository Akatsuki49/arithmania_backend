# from transformers import pipeline, DebertaV2TokenizerFast
# tokenizer = DebertaV2TokenizerFast.from_pretrained("model1-tokenizer")
# zeroshot_classifier = pipeline("zero-shot-classification",model='model1',tokenizer=tokenizer)
# text = "Angela Merkel is a politician in Germany and leader of the CDU"
# classes_verbalized = ["investment", "personal budgeting", "financial education"]
# output = zeroshot_classifier(text, classes_verbalized, multi_label=False)
# print(output)


# from transformers import pipeline, DebertaV2TokenizerFast
from openai import OpenAI
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def classify_question(question):
    # Initialize tokenizer and classifier
    # tokenizer = DebertaV2TokenizerFast.from_pretrained("model1-tokenizer")
    # zeroshot_classifier = pipeline("zero-shot-classification", model='model1', tokenizer=tokenizer)

    # # Text to classify
    # text = question

    # # Labels for classification
    # classes_verbalized = ["stock market", "personal budgeting", "financial education"]

    # # Perform classification
    # output = zeroshot_classifier(text, classes_verbalized, multi_label=False)

    # # Find the label with maximum confidence score
    # max_index = output['scores'].index(max(output['scores']))
    # classification = output['labels'][max_index]

    # API_KEY = "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"

    # prompt = '''

    # '''

    # client = OpenAI(api_key=API_KEY)
    # response = client.chat.completions.create(
    #     messages=[
    #         {"role": "user", "content": prompt}
    #     ],
    #     max_tokens=5,
    #     model="gpt-3.5",
    #     temperature=0.7,
    # )
    # classification = response.choices[0].message.content

    api_key = "8pPn2Ngk7v5wnqDzcqkEqQB73CeVkntH"
    model = "mistral-large-latest"

    client = MistralClient(api_key=api_key)

    content = f'''
{question}

Which category does this above statement belong to?

stock market
personal budgeting
financial education

Give the output as one of these 3 options only.
'''

    messages = [
        ChatMessage(role="user", content=content)
    ]

    # No streaming
    chat_response = client.chat(
        model=model,
        messages=messages,
    )

    print(chat_response.choices[0].message.content)
    return chat_response.choices[0].message.content
