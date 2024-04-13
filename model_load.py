from transformers import pipeline, DebertaV2TokenizerFast
tokenizer = DebertaV2TokenizerFast.from_pretrained("model1-tokenizer")
zeroshot_classifier = pipeline("zero-shot-classification",model='model1',tokenizer=tokenizer)
text = "Angela Merkel is a politician in Germany and leader of the CDU"
classes_verbalized = ["investment", "personal budgeting", "financial education"]
output = zeroshot_classifier(text, classes_verbalized, multi_label=False)
print(output)
