import pandas as pd
from src.models.sklearn.Naive_Bayes import naive_bayes_test


def test_allocine_naive_bayes():
    out_test = 'data/processed/results_nb_allocine.csv'
    in_test = 'src/tests/dataset_allocine_100.csv'
    accuracy = naive_bayes_test(in_test, out_test)
    assert accuracy > 0.5


def test_zemmour_naive_bayes():
    out_test = 'data/processed/results_nb_test_zemmour.csv'
    in_test = 'src/tests/Zemmour_135_tweets_labelled.csv'
    accuracy = naive_bayes_test(in_test, out_test)
    assert accuracy > 0.5
