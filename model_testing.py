from transformers import pipeline
zeroshot_classifier = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-large-zeroshot-v2.0")
zeroshot_classifier.model.save_pretrained("model1")
zeroshot_classifier.tokenizer.save_pretrained("model1-tokenizer")
