import pandas as pd
from src.models.huggingface.twitter_xlm_roberta_base_sentiment import huggin_face_predict, accuracy


def test_allocine_hugging_face():
    out_test = 'data/processed/aclImdb/results/results.csv'
    huggin_face_predict('src/tests/dataset_allocine_100.csv', out_test)
    df = pd.read_csv(out_test)
    assert accuracy(df) > 0.5


def test_zemmour_hugging_face():
    out_test = 'data/processed/aclImdb/results/results.csv'
    huggin_face_predict('src/tests/Zemmour_135_tweets_labelled.csv', out_test)
    df = pd.read_csv(out_test)
    assert accuracy(df) > 0.5
