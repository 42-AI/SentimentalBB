from src.models.sklearn.Naive_Bayes import Naive_Bayes
from src.models.ModelManager import ModelManager


def generic_test_for_nb(in_test, weights_test, dataset_type):
    mdl = Naive_Bayes()
    mm = ModelManager(mdl, dataset_type=dataset_type, flat_y=True)

    mm.train(in_test, weights_test)

    mm.load(weights_test)
    mm.test(in_test)
    mm.predict(in_test)


def test_allocine_naive_bayes():
    in_test = 'src/tests/dataset_allocine_100.csv'
    weights_test = "models/naive_bayes.test"

    generic_test_for_nb(in_test, weights_test, "bi")


def test_zemmour_naive_bayes():
    # out_test = "src/tests/test_set_240tweets_labeled_0410.csv"
    in_test = 'src/tests/Zemmour_135_tweets_labelled.csv'
    weights_test = "models/naive_bayes.test"

    generic_test_for_nb(in_test, weights_test, "bi")


def test_alexset_naive_bayes():
    in_test = "src/tests/test_set_240tweets_labeled_0410.csv"
    weights_test = "models/naive_bayes.test"

    generic_test_for_nb(in_test, weights_test, "bi")
