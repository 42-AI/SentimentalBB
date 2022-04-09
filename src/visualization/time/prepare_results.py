from src.data.load_dataset.twitter_predict import get_tweets_from_candidate
from src.models.huggingface.twitter_xlm_roberta_base_sentiment import HuggingFaceModel

import os
import pandas as pd


def get_day_predictions(model, tweets, day):
    X_prep = model.preprocess(tweets.tolist())
    y_pred = model.predict(X_prep)

    y_preds = pd.DataFrame(
        y_pred,
        columns=[
            'predict_Positive',
            'predict_Neutral',
            'predict_Negative'
        ]
    )
    y_preds["day"] = int(day)

    y_preds["preds_total"] = y_preds["predict_Positive"] + \
        y_preds["predict_Neutral"] + y_preds["predict_Negative"]
    y_preds["preds_not_positive"] = y_preds["predict_Neutral"] + \
        y_preds["predict_Negative"]
    return y_preds


def get_candidate_all_days_predictions(candidate):
    tweets = get_tweets_from_candidate(candidate)
    df = None
    hb = HuggingFaceModel()

    days = list(tweets.keys())
    days.sort()
    print(days)
    path_all_preds = f"data/processed/twitter/results/{candidate}_{days[0]}-{days[-1]}.csv"

    for i, (day, X) in enumerate(tweets.items()):
        print(f"{candidate} -> {i}/{len(days)}")
        path_day_pred = f"data/processed/twitter/results/{day}/{candidate}.csv"

        if os.path.exists(path_day_pred):
            y_preds = pd.read_csv(path_day_pred)
        else:
            y_preds = get_day_predictions(hb, X, day)
            os.makedirs(os.path.dirname(path_day_pred), exist_ok=True)
            y_preds.to_csv(path_day_pred)

        if type(df) == type(None):
            df = y_preds
        else:
            df = pd.concat([df, y_preds], axis=0)

        df.to_csv(path_all_preds)

    return df
