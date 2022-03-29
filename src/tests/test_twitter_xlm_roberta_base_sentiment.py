import pandas as pd
from src.models.huggingface import twitter_xlm_roberta_base_sentiment as model


def test():
    df = pd.read_csv('src/tests/dataset_allocine_100.csv')
    predict = df.apply(lambda row: model.pipe(row['review']), axis=1)

    def convert(label):
        if label == 'Positive':
            return 1
        elif label == 'Negative':
            return 0
        else:
            return -1
    df['y'] = predict.apply(lambda row: convert(row[0]['label']))
    true_y = df[(df['y'] == df['label'])].shape[0]
    accuracy = true_y / df.shape[0]
    print(f"Accuracy of {model.name} model on a sample of 100 examples\
            is: {accuracy}")
    assert accuracy > 0.5
