from src.models.ModelManager import ModelManager
from src.models.sklearn.Naive_Bayes import Naive_Bayes

import os
import pandas as pd


def pred_if_not_pred(base_path, ModelManager, candidate):
    for root_base, dirs, _ in os.walk(base_path, topdown=False):
        for day_dir in dirs:
            path_day = os.path.join(root_base, day_dir)
            for root_day, dirs, files in os.walk(path_day, topdown=False):
                for csv_candidate in files:
                    if csv_candidate.startswith(candidate):
                        path_candidate = os.path.join(root_day, csv_candidate)
                        if True or not os.path.exists(ModelManager.get_csv_out_from_csv_in(path_candidate)):
                            ModelManager.predict(path_candidate)


def complete_df(df, day):
    df["day"] = int(day)
    df["preds_total"] = df["predict_Positive"] + \
        df["predict_Neutral"] + df["predict_Negative"]
    df["preds_not_positive"] = df["predict_Neutral"] + \
        df["predict_Negative"]
    return df


def load_all_candidates_csv(result_dir, candidate):
    df = None
    for root_base, dirs, _ in os.walk(result_dir, topdown=False):
        for day_dir in dirs:
            path_day = os.path.join(root_base, day_dir)
            for root_day, dirs, files in os.walk(path_day, topdown=False):
                for csv_candidate in files:
                    if csv_candidate.startswith(candidate):
                        path_candidate = os.path.join(root_day, csv_candidate)

                        y_preds = pd.read_csv(path_candidate)
                        y_preds = complete_df(y_preds, day_dir)

                        if type(df) == type(None):
                            df = y_preds
                        else:
                            df = pd.concat([df, y_preds], axis=0)
    return df


def get_candidate_all_days_predictions(candidate, weights_in):
    base_dir = "data/processed/twitter/predict/"

    print(f"Candidate visu: {candidate}")
    mdl = Naive_Bayes()
    mm = ModelManager(mdl, dataset_type="predict", flat_y=False)
    mm.load(weights_in)

    print(f"Predicting new tweets...")
    pred_if_not_pred(base_dir, mm, candidate)

    print(f"Load all the candidate tweets...")
    result_dir = mm.get_csv_out_from_csv_in(base_dir)
    df = load_all_candidates_csv(result_dir, candidate)

    return df
