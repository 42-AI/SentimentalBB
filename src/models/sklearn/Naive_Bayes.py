import sklearn
from sklearn.naive_bayes import MultinomialNB as NB
import numpy as np
import pandas as pd
import scipy
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


class Naive_Bayes:
    """_summary_
    Multinomial Naive Bayes model based on hyperparam alpha = 1.
    - Multinomial Model only selected beacuse seems to be common practice
      for NLP (no thorough research done)
    - aplha set to 1 because default value (no iteration on alpha done)
    """

    def __init__(self):
        self.__clf = None

    def train(self, X_train: scipy.sparse.csr.csr_matrix,
              y_train: scipy.sparse.csr.csr_matrix):
        """
        X_train: {array-like, sparse matrix} of shape (n_samples, n_features)
        y_train: array-like of shape (n_samples,)
        """
        clf = NB().fit(X_train, y_train)
        self.__clf = clf

    def predict(self, X_test: scipy.sparse.csr.csr_matrix):
        predicted = self.__clf.predict(X_test)
        return predicted


def naive_bayes_train(csv_in, weights_out):
    print("--task train not implemented yet for naive-bayes")
    pass


def naive_bayes_test(csv_in, csv_out, weights_in=None, score='accuracy'):
    """

    Args:
        csv_in (_type_): _description_
        csv_out (_type_): _description_
        weights_in (_type_, optional): _description_. Defaults to None.
        score (str, optional): _description_. Defaults to 'accuracy'.
    """

    # ===================     PREPROCESS DATA    =============================

    df = pd.read_csv(csv_in)
    X = df[['text']]
    y = df[['Positive', 'Negative', 'Neutral']]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
    X_train = X_train.values
    X_test = X_test.values
    y_train_1d = y_train['Positive'] + (y_train['Negative'] * (-1))
    y_test_1d = y_test['Positive'] + (y_test['Negative'] * (-1))
    y_train_1d = y_train_1d.values
    y_test_1d = y_test_1d.values
    X_train = X_train.squeeze()
    X_test = X_test.squeeze()

    # ===================      VECTORIZATION    =============================

    # 1st step of vectorization: CountVectorizer vectorizes X_train and X_test
    vec = CountVectorizer()
    X_train_trans = vec.fit_transform(X_train)
    X_test_trans = vec.transform(X_test)

    # 2nd step: TF-IDF improves the vectorization of vectors created by
    #           CountVectorizer
    tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_trans)
    X_train_tf = tf_transformer.transform(X_train_trans)
    X_test_tf = tf_transformer.transform(X_test_trans)

    # ===================    TRAIN + PREDICT  ===============================

    nb = NB()
    nb.train(X_train_tf, y_train_1d)
    y_pred = nb.predict(X_test_tf)

    # ===================    EXPORT CSV_OUT    ===============================

    df["predict_Negative"] = (y_pred == -1).astype(int)
    df["predict_Neutral"] = (y_pred == 0).astype(int)
    df["predict_Positive"] = (y_pred == 1).astype(int)
    df.to_csv(csv_out)
    print(f"\nCsv with predictions created at {csv_out}\n")

    # ===================    PRINT SCORE       ===============================

    accuracy = sklearn.metrics.accuracy_score(y_test_1d, y_pred)
    print(f"Accuracy: {accuracy}")
    return (accuracy)


def naive_bayes_predict(csv_in, csv_out, weights_in=None):
    print("--task predict not implemented yet for naive-bayes")
    pass


def naive_bayes_main(args):
    if args.task == 'train':
        naive_bayes_train(args.train_csv, args.weights_out)
    elif args.task == 'test':
        naive_bayes_test(args.test_csv, args.out_csv)
    elif args.task == 'predict':
        naive_bayes_predict(args.predict_csv, args.csv_out)
