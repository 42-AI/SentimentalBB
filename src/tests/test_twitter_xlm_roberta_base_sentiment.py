#import pandas as pd
#from datasets import load_dataset
#import src.models.huggingface.twitter_xlm_roberta_base_sentiment as model


# def test():
#    dataset = load_dataset('allocine', split='test[:100]')
#    df = pd.DataFrame.from_dict(dataset)
#    df['predict'] = df.apply(lambda row: model.pipeline(row['review']), axis=1)
#    true_y = df[(df['predict'] == ['label'])].shape[0]
#    accuracy = true_y / df.shape[0]
#    print(
#        f"Accuracy of {model.name} model on a sample of 100 examples is: {accuracy}")
#    assert accuracy > 0.5
