import pandas as pd
from sklearn.model_selection import train_test_split
from src.data.load_dataset.base_dataset_tri_label import get_X_y
import os


def generic_test_for_hf(in_test, out_test):
    from src.models.huggingface.twitter_xlm_roberta_base_sentiment import (
        HuggingFaceModel,
        add_predictions_to_df
    )
    # Access data
    df = pd.read_csv(in_test)
    X, y = get_X_y(df)

    hf = HuggingFaceModel()

    # Test model
    y_pred = hf.predict(X.tolist())
    y_pred[y_pred != 0] = 1
    accuracy = hf.get_score(y, y_pred)
    # assert accuracy > 0.01

    # Wtrite results to disk
    df = add_predictions_to_df(df, y_pred)
    os.makedirs(os.path.dirname(out_test), exist_ok=True)
    df.to_csv(out_test)


def test_allocine_hugging_face():

    out_test = 'data/processed/aclImdb/results/results.csv'
    if "CI" in os.environ.keys():
        generic_test_for_hf('src/tests/dataset_allocine_100.csv', out_test)


def test_zemmour_hugging_face():
    out_test = 'data/processed/aclImdb/results/results.csv'
    if "CI" in os.environ.keys():
        generic_test_for_hf(
            'src/tests/Zemmour_135_tweets_labelled.csv', out_test)
