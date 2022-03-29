import sklearn
import numpy as np
import os
import joblib


class BaseModel:
    def __init__(self):
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

    def get_score(self, y_true, y_pred) -> float:
        accuracy = sklearn.metrics.accuracy_score(y_true, y_pred)
        return accuracy

    def load(self, path):
        return joblib.load(path)

    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self, path)
