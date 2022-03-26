from transformers import pipeline
import pandas as pd

# text,     label_1,    label_2,    label_3 [, predict_1,   predict_2,  predict_3   ]
# string,   0/1,        0/1,        0/1     [, 0-1,         0-1,        0-1         ]


def convert(label):
    if label == 'Positive':
        return 1
    elif label == 'Negative':
        return 0
    else:
        return -1


def accuracy(df, predict, name):
    df['y'] = predict.apply(lambda row : convert(row[0]['label']))
    true_y = df[(df['y'] == df['label'])].shape[0]
    accuracy = true_y / df.shape[0]
    print(f"Accuracy of {name} model on a sample of 100 examples is: {accuracy}")


def hf_predict(csv_in, csv_out):
    model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
    name = "twitter-xlm-roberta-base-sentiment"
    my_pipeline = pipeline("sentiment-analysis",
                        model=model_path, tokenizer=model_path)

    df = pd.DataFrame.from_csv(csv_in)

    predict = df.apply(lambda row : my_pipeline(row['text']), axis=1)
    # 'label': 'Positive'
    # 'score': 0.951051592826

    predict.DataFrame.to_csv(csv_out)
    accuracy(df, predict, name)
