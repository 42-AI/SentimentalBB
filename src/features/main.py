import os
import pandas as pd

from src.models.random import predict_model_random as random
from src.models.sklearn.Naive_Bayes import Naive_Bayes as NB
from src.models.huggingface import twitter_xlm_roberta_base_sentiment as xlm

RAW_PATH = 'data/raw'
SAVE_PATH = 'data/processed'

# ########################################################################### #
#                                 Functions                                   #
# ########################################################################### #


def dataset_to_csv(df_dataset: pd.DataFrame, filepath: str):
    """ Saves the dataset into a file in the specified directory.
    Args:
    -----
        df_dataset [pandas DataFrame]: dataframe containing the dataset.
        filepath [str]: path relative to SAVE_PATH of the file
            where df will be saved.
    Return:
    -------
        None
    """
    csv_path = f"{filepath}"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df_dataset.to_csv(csv_path)


def features_main(model: str, filepath: str):
    if os.path.isfile(f"{SAVE_PATH}/{model}/{filepath}"):
        print("This data is already processed!")
        return
    if not os.path.isfile(f"{RAW_PATH}/{filepath}"):
        print("This data does not exist!")
        return
    if model == 'random':
        pipe = random.pipe
    elif model == 'naive_bayes':
        pipe = NB.pipe
    elif model == 'twitter-xlm-roberta-base-sentiment':
        pipe = xlm.pipe
    df = pd.read_csv(f"{RAW_PATH}/{filepath}")
    predict = df.apply(lambda row: pipe(row['text']), axis=1)

    def convert(label):
        if (label == 'Positive'):
            return 1
        elif (label == 'Negative'):
            return -1
        elif (label == 'Neutral'):
            return 0

    df['label'] = predict.apply(lambda row: row[0]['label'])
    df['score'] = predict.apply(lambda row: row[0]['score'])
    df['convert'] = predict.apply(lambda row: convert(row[0]['label']))

    dataset_to_csv(df, f"{SAVE_PATH}/{model}/{filepath}")
