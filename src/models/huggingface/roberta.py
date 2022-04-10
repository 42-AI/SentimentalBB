from transformers import pipeline
import pandas as pd
import numpy as np

from src.models.BaseModel import BaseModel


class HuggingFaceModel(BaseModel):
    def __init__(self):
        model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
        name = "twitter-xlm-roberta-base-sentiment"
        self.my_pipeline = pipeline("sentiment-analysis",
                                    model=model_path, tokenizer=model_path)

    def preprocess(self, X: np.array):
        return X.tolist()

    def train(self, X_train: np.array, y_train: np.array):
        pass

    def _raw_y_to_y(self, raw_y):
        label = [r["label"] for r in raw_y]
        score = [r["score"] for r in raw_y]

        probas = [[
            int(l == "Positive") * s,
            int(l == "Negative") * s,
            int(l == "Neutral") * s,
        ] for l, s in zip(label, score)]

        y = np.array(probas)
        return y

    def predict(self, X: str):
        raw_y = self.my_pipeline(X)
        y = self._raw_y_to_y(raw_y)
        return y

    def add_predictions_to_df(self, df, y):
        y_preds = pd.DataFrame(y,
                               columns=[
                                   'predict_Positive',
                                   'predict_Neutral',
                                   'predict_Negative'])
        return pd.concat([df, y_preds], axis=1)


# def huggingface_train(csv_in, weights_out, weights_in=None):
#     raise NotImplementedError


# def huggingface_predict(csv_in, csv_out, weights_in):
#     df = pd.read_csv(csv_in)
#     X, _ = get_X_y(df)

#     # nb = HuggingFaceModel().load(weights_in)
#     hb = HuggingFaceModel()
#     X_prep = hb.preprocess(X.tolist())
#     y_pred = hb.predict(X_prep)

#     df = add_predictions_to_df(df, y_pred)
#     df.to_csv(csv_out)
#     print(f"\nCsv with predictions created at {csv_out}\n")


# def huggingface_test(csv_in, csv_out, weights_in, score='accuracy'):
#     df = pd.read_csv(csv_in)
#     X, y = get_X_y(df)

#     # nb = HuggingFaceModel().load(weights_in)
#     hb = HuggingFaceModel()
#     X_prep = hb.preprocess(X)
#     y_pred = hb.predict(X_prep)

#     print(f"{y = }")
#     print(f"{y_pred = }")
#     df = add_predictions_to_df(df, y_pred)

#     y_pred[y_pred != 0] = 1
#     accuracy = hb.get_score(y, y_pred)
#     print(f"Accuracy: {accuracy}")

#     df.to_csv(csv_out)
#     print(f"\nCsv with predictions created at {csv_out}\n")


# def huggingface_main(args):
#     if args.task == 'train':
#         huggingface_train(args.train_csv, args.weights_out, args.weights_in)
#     elif args.task == 'test':
#         huggingface_test(args.test_csv, args.out_csv, args.weights_in)
#     elif args.task == 'predict':
#         huggingface_predict(args.predict_csv, args.csv_out, args.weights_in)
