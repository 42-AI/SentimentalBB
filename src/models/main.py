from src.features.build_features import build_features_aclImdb as bf
from src.models.sklearn.Naive_Bayes import Naive_Bayes as NB
import pandas as pd
import argparse
import os

def add_models_args(parser):
    parser.add_argument('--train',
                            required=True,
                            help="Train set on which the model will train",
                            type=argparse.FileType('r')
                            )
    parser.add_argument('--test',
                            required=True,
                            help="Test set on which the model will be tested",
                            type=argparse.FileType('r')
                            )
    parser.add_argument('--predict',
                            required=True,
                            help="Test set on which the model will be tested",
                            type=argparse.FileType('r')
                            )
    parser.add_argument('--model',
                            help="Training based on the model entered",
                            default='random',
                            choices=['random', 'naive-bayes', 'hugging-face'],
                            )



def naive_bayes_main(train_csv, test_csv):
    X_train, X_test, y_train, y_test = bf(train_csv, test_csv)
    nb = NB()
    nb.train(X_train, y_train)
    y_pred = nb.predict(X_test)
    y_pred = pd.DataFrame(data=y_pred, columns=['y_pred'])
    y_test.reset_index(drop=True, inplace=True)
    y_test.columns = ['y_true']
    res = pd.concat([y_pred, y_test], axis=1)
    os.makedirs("data/processed/aclImdb/results", exist_ok=True)
    res.to_csv('data/processed/aclImdb/results/naivebayes.csv',
                header=['y_pred', 'y_true'])
    print("\n\ncsv 'naivebayes.csv' created at data/processed/aclImdb"
            "/results/.\n\nThe csv file contains two columns:\n"
            "- y_pred with all the predicted sentiments\n"
            "- y_true with all the true sentiments")


def models_main(args):
    """As of now, export a csv composed of two columns 'y_pred' and 'y_true'
       where y_pred has been found with the model passed as model_name.

    Args:
        train_csv (csv):
        test_csv (csv):
        model_name (str):
    """
    # bf works only for csvs with 3 columns where:
    #   - 1st column will be dropped
    #   - 2nd column represents the texts to analyse
    #   - 3rd column represents the sentiment {0,1}
    if args.model_name == "naive-bayes":
        naive_bayes_main(args.train_csv, args.test_csv)
    elif args.model_name == "hugging-face":
        if 
    else:
        print("Other models than Naive-Bayes not implemented yet")
