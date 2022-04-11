import pandas as pd
import numpy as np
from unidecode import unidecode
import os

from src import config


def get_tweets_csv(csv_path: str) -> np.array:
    df = pd.read_csv(csv_path)
    X = df['text'].apply(lambda row: unidecode(row)).to_numpy()
    return X


def get_tweets_df(df) -> np.array:
    X = df['text'].apply(lambda row: unidecode(row)).to_numpy()
    return X
