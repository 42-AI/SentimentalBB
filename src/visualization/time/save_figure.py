
from src.data.load_dataset.twitter_predict import get_tweets_from_candidate
import seaborn as sn
from src.models.huggingface.twitter_xlm_roberta_base_sentiment import HuggingFaceModel
import pandas as pd


def save_figure_candidate(candidate):
    tweets = get_tweets_from_candidate(candidate)

    hb = HuggingFaceModel()
    for day, X in tweets.items():
        X_prep = hb.preprocess(X.tolist())
        y_pred = hb.predict(X_prep)

        y_preds = pd.DataFrame(y_pred,
                               columns=[
                                   'predict_Positive',
                                   'predict_Neutral',
                                   'predict_Negative'])
        pass
