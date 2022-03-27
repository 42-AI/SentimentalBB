import pandas as pd


def test_naive_bayes():
    df = pd.read_csv('data/processed/aclImdb/results/naivebayes.csv')
    tp = df[(df['y_pred'] == 1) & (df['y_true'] == 1)].shape[0]
    tn = df[(df['y_pred'] == 0) & (df['y_true'] == 0)].shape[0]
    fp = df[(df['y_pred'] == 1) & (df['y_true'] == 0)].shape[0]
    fn = df[(df['y_pred'] == 0) & (df['y_true'] == 1)].shape[0]
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    print(f"Accuracy of Naive Bayes model on aclImdb: {accuracy}")
    assert accuracy > 0.5
