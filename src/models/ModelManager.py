from src.models.BaseModel import BaseModel
from src.data.load_dataset.base_dataset_tri_label import get_X_y_tri
from src.data.load_dataset.base_dataset_bi_label import get_X_y_bi
from src.data.load_dataset.twitter_predict import get_tweets_df
import pandas as pd
import numpy as np

import os


class ModelManager():
    def __init__(self, model: BaseModel, dataset_type="bi", flat_y=False) -> None:
        self.model = model
        self.dataset_type = dataset_type
        self.flat_y = flat_y
        self.model_name = type(self.model).__name__

        self.path_testset = "src/tests/test_set_240tweets_labeled_0410.csv"

        self.weights_in = "no_weights_in"

        indent = 4
        print(f"Model manager: {self.model_name}")
        print(f"{' ' * indent}{flat_y = }")
        print(f"{' ' * indent}{dataset_type = }")

    def load(self, weights_in):
        if weights_in:
            self.weights_in = weights_in
            self.model = self.model.load(weights_in)

    def get_X_y(self, csv_in):
        self.df = pd.read_csv(csv_in)
        if self.dataset_type == "bi":
            X, y = get_X_y_bi(self.df, flat_y=self.flat_y)
        elif self.dataset_type == "tri":
            X, y = get_X_y_tri(self.df, flat_y=self.flat_y)
        elif self.dataset_type == "predict":
            X = get_tweets_df(self.df)
            y = np.array([0])
        else:
            raise ValueError(
                f"ERROR: dataset_type should be 'bi' or 'tri', not: {self.dataset_type}")
        # print(f"{X.shape = }")
        # print(f"{y.shape = }")
        return X, y

    def test(self, csv_in, score='accuracy'):
        X, y = self.get_X_y(csv_in)

        X_prep = self.model.preprocess(X)
        y_pred = self.model.predict(X_prep)

        y_pred[y_pred != 0] = 1

        # print(f"{y_pred.shape = }")
        # print(f"{y.shape = }")

        if not self.flat_y:
            y = np.argmax(y, axis=1)
            y_pred = np.argmax(y_pred, axis=1)

        accuracy = self.model.get_score(y, y_pred)
        print(f"Accuracy of {self.model_name} is {accuracy}")
        return accuracy

    def train(self, csv_in, weights_out):
        X, y = self.get_X_y(csv_in)

        X_prep = self.model.preprocess(X)
        y_pred = self.model.train(X_prep, y)

        acc = self.test(self.path_testset)
        s_acc = f"{int(100 * acc):03}"
        self.model.save(weights_out, s_acc)

    def get_csv_out_from_csv_in(self, csv_in):
        mdl_name = os.path.basename(self.weights_in).split(".")[0]
        csv_out = csv_in.replace("/predict/", f"/results/{mdl_name}/")
        return csv_out

    def predict(self, csv_in, csv_out=None):
        X, y = self.get_X_y(csv_in)

        X_prep = self.model.preprocess(X)
        y_pred = self.model.predict(X_prep)

        self.df = self.model.add_predictions_to_df(self.df, y_pred)

        if csv_out == None:
            csv_out = self.get_csv_out_from_csv_in(csv_in)

        os.makedirs(os.path.dirname(csv_out), exist_ok=True)
        self.df.to_csv(csv_out)
        return self.df
