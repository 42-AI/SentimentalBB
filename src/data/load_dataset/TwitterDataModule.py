from typing import Optional, Tuple

import torch
from pytorch_lightning import LightningDataModule
from torch.utils.data import ConcatDataset, DataLoader, Dataset, random_split
from torchvision.datasets import MNIST
from torchvision.transforms import transforms

from torch.utils.data import DataLoader
from torch.utils.data import Dataset
import pandas as pd
from src.data.load_dataset.base_dataset_bi_label import get_X_y_bi


class OurDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


class TwitterDataModule(LightningDataModule):
    """Example of LightningDataModule for MNIST dataset. A DataModule implements 5 key methods:
            - prepare_data (things to do on 1 GPU/TPU, not on every GPU/TPU in distributed mode)
            - setup (things to do on every accelerator in distributed mode)
            - train_dataloader (the training dataloader)
            - val_dataloader (the validation dataloader(s))
            - test_dataloader (the test dataloader(s))
    This allows you to share a full dataset without explaining how to download,
    split, transform and process the data.
    Read the docs:
            https://pytorch-lightning.readthedocs.io/en/latest/extensions/datamodules.html
    """

    def __init__(self,
                 csv_test_path="src/tests/test_set_240tweets_labeled_0410.csv",
                 csv_train_path="data/processed/allocine/allocine_trainset_160000reviews.csv",
                 ):
        super().__init__()
        self.csv_test_path = csv_test_path
        self.csv_train_path = csv_train_path

    def setup(self, stage: Optional[str] = None):
        """Load data.
        Set variables: `self.data_train`, `self.data_val`, `self.data_test`. This method is
        called by lightning when doing `trainer.fit()` and `trainer.test()`, so be careful
        not to execute the random split twice! The `stage` can be used to differentiate
        whether it's called before trainer.fit()` or `trainer.test()`.
        """

        self.df_test = pd.read_csv(self.csv_test_path)
        X_test, y_test = get_X_y_bi(self.df_test)
        self.dataset_test = OurDataset(X_test, y_test)

        self.df_train = pd.read_csv(self.csv_train_path)
        X_train, y_train = get_X_y_bi(self.df_train)
        self.dataset_train = OurDataset(X_train, y_train)

        size_train = int(len(self.dataset_train) * 0.8)
        size_val = len(self.dataset_train) - (size_train)

        self.data_test = self.dataset_test
        self.data_train, self.data_val = random_split(
            dataset=self.dataset_train,
            lengths=[size_train, size_val],
            generator=torch.Generator().manual_seed(42),
        )

    def train_dataloader(self):
        return DataLoader(
            dataset=self.data_train,
            batch_size=8,
            num_workers=1,
            shuffle=True,
        )

    def val_dataloader(self):
        return DataLoader(
            dataset=self.data_val,
            batch_size=8,
            num_workers=1,
            shuffle=True,
        )

    def test_dataloader(self):
        return DataLoader(
            dataset=self.data_test,
            batch_size=8,
            num_workers=1,
            shuffle=True,
        )
