from transformers import pipeline

model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
name = "twitter-xlm-roberta-base-sentiment"
pipe = pipeline("sentiment-analysis",
                model=model_path, tokenizer=model_path)
