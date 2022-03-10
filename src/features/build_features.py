import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


def build_features_aclImdb(train_csv: str, test_csv: str):
    """Summary:
        - Clean csvs
        - Split train and test into X_train/y_train and X_test/y_test
        - Vectorize the texts using TF-IDF: creates n_features for each text
          where n = number of different tokens(words) in all the texts in
          train_csv

    Args:
        train_csv (csv): 3 columns(unused, text, sentiment{0,1}) and n examples
        test_csv (csv): 3 columns(unused, text, sentiment{0,1}) and n examples

    Returns:
        X_train_tf: <'scipy.sparse._csr.csr_matrix'> of shape (n, nb_features)
        X_test_tf: <'scipy.sparse._csr.csr_matrix'> of shape (n, nb_features)
        y_train: <'numpy.ndarray'> of shape (n,)
        X_train: <'pandas.core.series.Series'> of shape (n,)

    """
    # transform csvs into dataframes
    df_train = pd.read_csv(train_csv)
    df_test = pd.read_csv(test_csv)
    # drop 1st unused column
    df_train = df_train.drop(df_train.columns[0], axis=1)
    df_test = df_test.drop(df_test.columns[0], axis=1)
    # Shuffle the datasets
    df_train = df_train.sample(frac=1)
    df_test = df_test.sample(frac=1)
    # Split datasets into X and y
    X_train = df_train['text']
    y_train = df_train['sentiment']
    X_test = df_test['text']
    y_test = df_test['sentiment']
    # Transform pd objects into np objects
    X_train = X_train.values
    y_train = y_train.values

    # ===================      VECTORIZATION    =============================

    # 1st step of vectorization: CountVectorizer vectorizes X_train and X_test
    vec = CountVectorizer(stop_words='english')
    X_train_trans = vec.fit_transform(X_train)
    X_test_trans = vec.transform(X_test)
    # 2nd step: TF-IDF improves the vectorization of vectors created by
    #           CountVectorizer
    tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_trans)
    X_train_tf = tf_transformer.transform(X_train_trans)
    X_test_tf = tf_transformer.transform(X_test_trans)
    return X_train_tf, X_test_tf, y_train, y_test
