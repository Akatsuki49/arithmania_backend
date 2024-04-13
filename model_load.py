# from transformers import pipeline, DebertaV2TokenizerFast
# tokenizer = DebertaV2TokenizerFast.from_pretrained("model1-tokenizer")
# zeroshot_classifier = pipeline("zero-shot-classification",model='model1',tokenizer=tokenizer)
# text = "Angela Merkel is a politician in Germany and leader of the CDU"
# classes_verbalized = ["investment", "personal budgeting", "financial education"]
# output = zeroshot_classifier(text, classes_verbalized, multi_label=False)
# print(output)


from transformers import pipeline, DebertaV2TokenizerFast

def classify_question(question):
    # Initialize tokenizer and classifier
    tokenizer = DebertaV2TokenizerFast.from_pretrained("model1-tokenizer")
    zeroshot_classifier = pipeline("zero-shot-classification", model='model1', tokenizer=tokenizer)
    
    # Text to classify
    text = question
    
    # Labels for classification
    classes_verbalized = ["investment", "personal budgeting", "financial education"]
    
    # Perform classification
    output = zeroshot_classifier(text, classes_verbalized, multi_label=False)
    
    # Find the label with maximum confidence score
    max_index = output['scores'].index(max(output['scores']))
    classification = output['labels'][max_index]
    
    return classification



# Example usage
text = "Angela Merkel is a politician in Germany and leader of the CDU"
classification_result = classify_question(text)
print(classification_result)
