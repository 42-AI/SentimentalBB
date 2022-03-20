from transformers import pipeline

model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
pipeline = pipeline("sentiment-analysis",
                    model=model_path, tokenizer=model_path)
