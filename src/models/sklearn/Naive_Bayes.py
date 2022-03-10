import sklearn
from sklearn.naive_bayes import MultinomialNB
import numpy as np


class Naive_Bayes:
    """_summary_
    Multinomial Naive Bayes model based on hyperparam alpha = 1.
    - Multinomial Model only selected beacuse seems to be common practice
      for NLP (no thorough research done)
    - aplha set to 1 because default value (no iteration on alpha done)
    """

    def __init__(self):
        self.__clf = None

    def train(self, X_train, y_train):
        """
        X_train: {array-like, sparse matrix} of shape (n_samples, n_features)
        y_train: array-like of shape (n_samples,)
        """
        clf = MultinomialNB().fit(X_train, y_train)
        self.__clf = clf

    def predict(self, X_test):
        predicted = self.__clf.predict(X_test)
        return predicted
