from src.data.make_dataset.aclImdb import make_dataset_aclImdb
from src.data.make_dataset.macron import make_dataset_macron


def data_main(dataset_download: str):
    if dataset_download == "aclImdb":
        make_dataset_aclImdb()
    elif dataset_download == "macron":
        make_dataset_macron()
