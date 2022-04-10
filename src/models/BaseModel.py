import sklearn
import numpy as np
import os
import joblib

from datetime import datetime


class BaseModel:
    def __init__(self, **kwargs):
        pass

    def add_argparse_args(self, parser):
        pass

    def train(self, X_train: np.array,
              y_train: np.array):
        """
        X_train: {array-like, sparse matrix} of shape (n_samples, n_features)
        y_train: array-like of shape (n_samples,)
        """
        raise NotImplementedError

    def preprocess(self, X: np.array):
        return X

    def predict(self, X: np.array):
        raise NotImplementedError

    def get_score(self, y_true: np.array, y_pred: np.array) -> float:
        accuracy = sklearn.metrics.accuracy_score(y_true, y_pred)
        return accuracy

    def load(self, path):
        return joblib.load(path)

    def save(self, path=None, acc="XXX"):
        if path == None:
            date = datetime.now().strftime("%m-%d_%H:%M")
            name = type(self).__name__
            path = f"./models/{acc}_{name}_{date}.z"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self, path)
