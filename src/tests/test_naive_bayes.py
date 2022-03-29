import pandas as pd
from sklearn.model_selection import train_test_split
from src.data.load_dataset.base_dataset_tri_label import get_X_y
from src.models.sklearn.Naive_Bayes import Naive_Bayes, add_predictions_to_df


def generic_test_for_nb(in_test, weights_test, out_test):
    # Access data
    df = pd.read_csv(in_test)
    X, y = get_X_y(df)

    # Test load and save
    nb = Naive_Bayes()
    nb.save(weights_test)
    nb = nb.load(weights_test)

    # Model pipeline
    X_prep = nb.preprocess(X)
    # Splitting after preprocessing
    X_train, X_test, y_train, y_test = train_test_split(
        X_prep, y, test_size=0.5)
    nb.train(X_train, y_train)

    # Test model
    y_pred = nb.predict(X_test)
    accuracy = nb.get_score(y_test, y_pred)
    assert accuracy > 0.5

    # Wtrite results to disk
    y_pred = nb.predict(X_prep)
    df = add_predictions_to_df(df, y_pred)
    df.to_csv(out_test)


def test_allocine_naive_bayes():
    # Constants
    out_test = 'data/processed/results_nb_allocine.csv'
    in_test = 'src/tests/dataset_allocine_100.csv'
    weights_test = "models/naive_bayes.test"

    generic_test_for_nb(in_test, weights_test, out_test)


def test_zemmour_naive_bayes():
    # Constants
    out_test = 'data/processed/results_nb_test_zemmour.csv'
    in_test = 'src/tests/Zemmour_135_tweets_labelled.csv'
    weights_test = "models/naive_bayes.test"

    generic_test_for_nb(in_test, weights_test, out_test)
