import sklearn
import joblib
import os
import numpy as np
import random

from src.models.BaseModel import BaseModel


class RandomModel(BaseModel):
    def __init__(self):
        pass

    def train(self, X_train: np.array, y_train: np.array):
        """
        X_train: {array-like, sparse matrix} of shape (n_samples, n_features)
        y_train: array-like of shape (n_samples,)
        """
        pass

    def predict(self, X: np.array):
        a = np.random.rand(X.shape[0], 3)
        b = np.zeros_like(a)
        b[np.arange(len(a)), a.argmax(1)] = 1
        return b
