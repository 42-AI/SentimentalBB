import pandas as pd
import numpy as np
from unidecode import unidecode
import os

from src import config


def get_tweets(csv_path: str) -> np.array:
    df = pd.read_csv(csv_path)
    X = df['text'].apply(lambda row: unidecode(row)).to_numpy()
    return X


def get_tweets_df(df) -> np.array:
    X = df['text'].apply(lambda row: unidecode(row)).to_numpy()
    return X


def get_tweets_from_candidate(
    candidate,
    predict_path="data/processed/twitter/predict/"
):
    candidate_dic = {}
    for root_base, dirs, _ in os.walk(predict_path, topdown=False):
        for day_dir in dirs:
            path_day = os.path.join(root_base, day_dir)
            for root_day, dirs, files in os.walk(path_day, topdown=False):
                for csv_candidate in files:

                    s_candidat, s_date, _ = csv_candidate.split("_")

                    if s_candidat == candidate:

                        path_candidate = os.path.join(root_day, csv_candidate)
                        tweets = get_tweets(path_candidate)

                        candidate_dic[s_date] = tweets

                        print(f"{s_candidat}: {s_date} -> {tweets.shape}")
    return candidate_dic


def get_tweets_from_candidates(predict_path="data/processed/twitter/predict/"):
    candidate_dic = {}
    for candidate in config.lst_candidats_file_name:
        tweets = get_tweets_from_candidate(
            candidate, predict_path=predict_path)
        print(f"{candidate}: {tweets.keys()}")
        candidate_dic[candidate] = tweets
    return candidate_dic


def my_test_main():
    get_tweets_from_candidates()
