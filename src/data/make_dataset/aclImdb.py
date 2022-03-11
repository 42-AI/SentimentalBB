import csv
import pandas as pd

import os


def make_set(dir_in: str, set_type: str):
    """Convert raw summary.json data to processed pick_and_bans data

    Arguments:
        path_in [str]: path to summary.json in raw data

    Returns:
        pandas.Dataframe
    """
    pre_df = {
        "text": [],
        "sentiment": [],
    }
    for root, dirs, files in os.walk(f"{dir_in}/pos", topdown=False):
        for name in files:
            path_in = os.path.join(root, name)
            with open(path_in, 'r') as f:
                pre_df['text'].append(f.read())
                pre_df['sentiment'].append(1)

    for root, dirs, files in os.walk(f"{dir_in}/neg", topdown=False):
        for name in files:
            path_in = os.path.join(root, name)
            with open(path_in, 'r') as f:
                pre_df['text'].append(f.read())
                pre_df['sentiment'].append(0)

    df = pd.DataFrame.from_dict(pre_df)
    csv_path = f"data/processed/aclImdb/aclImdb_{set_type}.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df.to_csv(csv_path)


def make_dataset_aclImdb():
    make_set("data/raw/StandfordSentiments/aclImdb/aclImdb/train", "train")
    make_set("data/raw/StandfordSentiments/aclImdb/aclImdb/test", "test")
