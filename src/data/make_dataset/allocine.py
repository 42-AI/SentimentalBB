from datasets import load_dataset
import pandas as pd
import os


csv_dest = "data/processed/allocine/"


def make_dataset_allocine(split: str="test"):
    dataset = load_dataset('allocine', split=split)
    print(dataset[0])

    pre_df = {
        "text": [datapoint["review"] for datapoint in dataset],
        "sentiment": [datapoint["label"] for datapoint in dataset],
    }
    df = pd.DataFrame.from_dict(pre_df)
    csv_path = f"{csv_dest}{split}.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df.to_csv(csv_path)
