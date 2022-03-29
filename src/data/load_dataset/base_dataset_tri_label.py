import pandas as pd
import numpy as np
from typing import List, Tuple
from unidecode import unidecode


def get_X(df: pd.DataFrame) -> np.array:
    X = df['text'].to_numpy()
    X = df['text'].apply(lambda row: unidecode(row)).to_numpy()
    print(f"{X = }")
    return X


def get_y(df: pd.DataFrame) -> np.array:
    y = df[['Positive', 'Negative', 'Neutral']].to_numpy()
    # https://stackoverflow.com/questions/45183213/coverting-back-one-hot-encoded-results-back-to-single-column-in-python
    y_labels = np.argmax(y, axis=1)
    return y_labels


def get_X_y(df: pd.DataFrame) -> Tuple[np.array, np.array]:
    X = get_X(df)
    y = get_y(df)
    return X, y
