import os
import pandas as pd
import

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
    csv_path = f"{SAVE_PATH}/{filepath}.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df_dataset.to_csv(csv_path)


def features_main(model: str, data: str):
    from src.models import model
    df = pd.read_csv(f"{RAW_PATH}/{data}")
    predict = df.apply(lambda row : model.pipe(row['review']), axis=1)
    def convert(label):
        if label == 'Positive':
            return 1
        elif label == 'Negative':
            return 0
        else:
            return -1
    df['y'] = predict.apply(lambda row : convert([row[0]['label']))
    df['score'] = predict.apply(lambda row : [row[0]['score'])

