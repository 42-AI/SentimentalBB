import pandas as pd
import os
import sys
from datasets import load_dataset


def make_dataset_allocine(args):
    # Check for parsing errors
    if args.split not in ["test", "train"]:
        print("--split argument is required for allocine: [train, test]")
        sys.exit()
    if args.split == 'train':
        EXPORT_PATH = "./data/processed/allocine"
    else:
        EXPORT_PATH = "./src/tests"
    # Download dataset allocine from Huggingface
    print("Downloading dataset allocine.....")
    dataset = load_dataset('allocine', split=args.split)
    print("Dataset allocine downloaded")
    # Convert dataset to pd dataframe
    pre_df = {
        "text": [datapoint["review"] for datapoint in dataset],
        "Positive": [datapoint["label"] for datapoint in dataset],
    }
    df = pd.DataFrame.from_dict(pre_df)
    df['Negative'] = abs(df['Positive'] - 1)
    # Use Case --split is test
    nb_reviews = int(args.nb_reviews)
    if args.split == 'test':
        if nb_reviews < 1 or nb_reviews > 10000:
            print("nb_reviews should be in range [1-10000]")
            sys.exit()
        df = df.sample(n=nb_reviews)
        df = df.reset_index()
        df = df.drop('index', axis=1)
    # exporting to csv
    os.makedirs(EXPORT_PATH, exist_ok=True)
    df.to_csv(f"{EXPORT_PATH}/allocine_{args.split}set_{len(df)}reviews.csv")
    print(f"Csv created as {EXPORT_PATH}/allocine_{args.split}"
          f"set_{len(df)}reviews.csv")
