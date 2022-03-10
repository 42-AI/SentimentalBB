import pandas as pd


def test_naive_bayes():
    df = pd.read_csv('data/processed/aclImdb/results/naivebayes.csv')
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for i, row in df.iterrows():
        if row['y_pred'] == 0 and row['y_true'] == 0:
            tn += 1
        if row['y_pred'] == 0 and row['y_true'] == 1:
            fn += 1
        if row['y_pred'] == 1 and row['y_true'] == 0:
            fp += 1
        if row['y_pred'] == 1 and row['y_true'] == 1:
            tp += 1
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    print(f"Accuracy of Naive Bayes model on aclImdb: {accuracy}")
    assert accuracy > 0.5
