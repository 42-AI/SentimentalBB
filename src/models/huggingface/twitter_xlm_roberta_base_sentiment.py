from transformers import pipeline
import pandas as pd
from sklearn.metrics import accuracy_score

# text,     label_1,    label_2,    label_3 [, predict_1,   predict_2,  predict_3   ]
# string,   0/1,        0/1,        0/1     [, 0-1,         0-1,        0-1         ]


def convert(label):
    if label == 'Positive':
        return 1
    elif label == 'Negative':
        return 0
    else:
        return -1


def accuracy(df):
    df['predict_Positive'] = df.apply(
        lambda row: 1 if row["predict_Positive"] > 0 else 0, axis=1)
    df['predict_Negative'] = df.apply(
        lambda row: 1 if row["predict_Negative"] > 0 else 0, axis=1)
    df['predict_Neutral'] = df.apply(
        lambda row: 1 if row["predict_Neutral"] > 0 else 0, axis=1)

    labels = df[['Positive', 'Negative', 'Neutral']].to_numpy()
    predis = df[['predict_Positive', 'predict_Negative',
                 'predict_Neutral']].to_numpy()

    accuracy = accuracy_score(labels, predis)
    print(f"Total accuracy is {accuracy_score(labels, predis)}")
    for i, label in enumerate(['Positive', 'Negative', 'Neutral']):
        print(
            f"{' ' * 4}{label} accuracy is {accuracy_score(labels[:,i], predis[:,i])}")
    return accuracy


def huggin_face_predict(csv_in, csv_out):
    model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
    name = "twitter-xlm-roberta-base-sentiment"
    my_pipeline = pipeline("sentiment-analysis",
                           model=model_path, tokenizer=model_path)

    df = pd.read_csv(csv_in)

    predict = df.apply(lambda row: my_pipeline(row['text']), axis=1)
    df["raw_pred"] = predict
    new_pred_label = df.apply(lambda row: row["raw_pred"][0]["label"], axis=1)
    new_pred_score = df.apply(lambda row: row["raw_pred"][0]["score"], axis=1)
    df["predict_Negative"] = (new_pred_label == "Negative").astype(int)
    df["predict_Neutral"] = (new_pred_label == "Neutral").astype(int)
    df["predict_Positive"] = (new_pred_label == "Positive").astype(int)
    df["predict_Positive"] = df["predict_Positive"] * new_pred_score
    df["predict_Negative"] = df["predict_Negative"] * new_pred_score
    df["predict_Neutral"] = df["predict_Neutral"] * new_pred_score
    df = df[['text', 'Positive', 'Negative', 'Neutral',
            'predict_Negative', 'predict_Positive', 'predict_Neutral']]
    df.to_csv(csv_out)
    acc = accuracy(df)
    print(f"Accuracy of {name} model on a sample of 100 examples is: {acc}")
    return acc
