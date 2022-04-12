import sklearn
from sklearn.naive_bayes import MultinomialNB as NB
import pandas as pd
import numpy as np
import scipy
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import joblib
from src.data.load_dataset.base_dataset_tri_label import get_X_y_tri
from src.data.load_dataset.base_dataset_bi_label import get_X_y_bi
from src.models.BaseModel import BaseModel


class Naive_Bayes(BaseModel):
    """_summary_
    Multinomial Naive Bayes model based on hyperparam alpha = 1.
    - Multinomial Model only selected beacuse seems to be common practice
      for NLP (no thorough research done)
    - aplha set to 1 because default value (no iteration on alpha done)
    """

    def __init__(self):
        self.__clf = NB(alpha=1)
        self.trained_preprocessing = False

    def train(self, X_train: scipy.sparse.csr.csr_matrix,
              y_train: scipy.sparse.csr.csr_matrix):
        """
        X_train: {array-like, sparse matrix} of shape (n_samples, n_features)
        y_train: array-like of shape (n_samples,)
        """
        self.__clf = self.__clf.fit(X_train, y_train)

    def preprocess(self, X):
        if not self.trained_preprocessing:
            self.vec = CountVectorizer()
            # 1st step of vectorization: CountVectorizer vectorizes X_train and X_test
            _ = self.vec.fit_transform(X)
            # # 2nd step: TF-IDF improves the vectorization of vectors created by
            # #           CountVectorizer
            # self.tf_transformer = TfidfTransformer(use_idf=False).fit(X)
            self.trained_preprocessing = True

        X_vec = self.vec.transform(X)
        # X_tf = self.tf_transformer.transform(X_vec)
        return X_vec

    def one_hot_y(self, y):
        nb_features = 3
        b = np.zeros((y.size, nb_features))
        b[np.arange(y.size), y] = 1
        return b

    def predict(self, X: scipy.sparse.csr.csr_matrix):
        predicted = self.__clf.predict(X)
        matrix_predicted = self.one_hot_y(predicted)
        return matrix_predicted

    def add_predictions_to_df(self, df, y):
        y_preds = pd.DataFrame(y,
                               columns=[
                                   'predict_Positive',
                                   'predict_Negative',
                                   'predict_Neutral',
                               ]
                               )
        return pd.concat([df, y_preds], axis=1)


# def naive_bayes_train(csv_in, weights_out, weights_in=None):
#     df = pd.read_csv(csv_in)
#     X, y = get_X_y_tri(df, flat_y=True)

#     if weights_in:
#         nb = Naive_Bayes().load(weights_in)
#     else:
#         nb = Naive_Bayes()
#     X_prep = nb.preprocess(X)
#     nb.train(X_prep, y)

#     nb.save(weights_out)


# def naive_bayes_predict(csv_in, csv_out, weights_in):
#     df = pd.read_csv(csv_in)
#     X, _ = get_X_y_tri(df, flat_y=True)

#     nb = Naive_Bayes().load(weights_in)
#     X_prep = nb.preprocess(X)
#     y_pred = nb.predict(X_prep)

#     df = add_predictions_to_df(df, y_pred)
#     df.to_csv(csv_out)
#     print(f"\nCsv with predictions created at {csv_out}\n")


# def naive_bayes_test(csv_in, csv_out, weights_in, score='accuracy'):
#     df = pd.read_csv(csv_in)
#     X, y = get_X_y_tri(df, flat_y=True)

#     nb = Naive_Bayes().load(weights_in)
#     X_prep = nb.preprocess(X)
#     y_pred = nb.predict(X_prep)

#     accuracy = nb.get_score(y, y_pred)
#     print(f"Accuracy: {accuracy}")

#     df.to_csv(csv_out)
#     print(f"\nCsv with predictions created at {csv_out}\n")


# def naive_bayes_alex(csv_in, csv_out, weights_in=None, score='accuracy'):
#     """

#     Args:
#             csv_in (_type_): _description_
#             csv_out (_type_): _description_
#             weights_in (_type_, optional): _description_. Defaults to None.
#             score (str, optional): _description_. Defaults to 'accuracy'.
#     """
#     # ===================     PREPROCESS DATA    =============================

#     df = pd.read_csv(csv_in)
#     X = df[['text']]
#     y = df[['Positive', 'Negative', 'Neutral']]
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
#     X_train = X_train.values
#     X_test = X_test.values
#     y_train_1d = y_train['Positive'] + (y_train['Negative'] * (-1))
#     y_test_1d = y_test['Positive'] + (y_test['Negative'] * (-1))
#     y_train_1d = y_train_1d.values
#     y_test_1d = y_test_1d.values
#     X_train = X_train.squeeze()
#     X_test = X_test.squeeze()

#     # ===================      VECTORIZATION    =============================

#     # 1st step of vectorization: CountVectorizer vectorizes X_train and X_test
#     vec = CountVectorizer()
#     X_train_trans = vec.fit_transform(X_train)
#     X_test_trans = vec.transform(X_test)

#     # 2nd step: TF-IDF improves the vectorization of vectors created by
#     #           CountVectorizer
#     tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_trans)
#     X_train_tf = tf_transformer.transform(X_train_trans)
#     X_test_tf = tf_transformer.transform(X_test_trans)

#     # ===================    TRAIN + PREDICT  ===============================

#     nb = NB()
#     nb.train(X_train_tf, y_train_1d)
#     y_pred = nb.predict(X_test_tf)

#     # ===================    EXPORT CSV_OUT    ===============================

#     df["predict_Negative"] = (y_pred == -1).astype(int)
#     df["predict_Neutral"] = (y_pred == 0).astype(int)
#     df["predict_Positive"] = (y_pred == 1).astype(int)
#     df.to_csv(csv_out)
#     print(f"\nCsv with predictions created at {csv_out}\n")

#     # ===================    PRINT SCORE       ===============================

#     accuracy = sklearn.metrics.accuracy_score(y_test_1d, y_pred)
#     print(f"Accuracy: {accuracy}")
#     return (accuracy)


# def naive_bayes_main(args):
#     if args.task == 'train':
#         naive_bayes_train(args.train_csv, args.weights_out, args.weights_in)
#     elif args.task == 'test':
#         naive_bayes_test(args.test_csv, args.out_csv, args.weights_in)
#     elif args.task == 'predict':
#         naive_bayes_predict(args.predict_csv, args.csv_out, args.weights_in)
