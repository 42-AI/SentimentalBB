from src.data.make_dataset.aclImdb import make_dataset_aclImdb
from src.data.make_dataset.allocine import make_dataset_allocine
from src.data.download.download_tweets import download_tweets

# ########################################################################### #
#                                 Constants                                   #
# ########################################################################### #


# ########################################################################### #
#                                 Functions                                   #
# ########################################################################### #

def data_main(dataset: str, split: str, txt: str, mention: str, start_time: str, end_time: str, tweet_fields: str):
    """ Main function to interact with the Twitter API or with aclImdb.
    It downloads and save the dataset/result into a file.
    Args:
    -----
        dataset [str]: type of dataset/API one wish to interact with.
        split[str]: specify the configuration (train or test)
        txt [str]: text one wish to be present within the tweets.
        mention [str]: mention of a candidat in the forged request.
        start_time [str]: starting date from which tweets will be download.
        end_time [str]: ending date until which tweets will be download.
        tweet_fields[str]: specify the tweet fields. Defaults is 'id,created_at,text'.
    Return:
    -------
        None
    Remarks:
    --------
        dataset parameter value must be in ['twitter', 'aclImdb', 'allocine']
        mention parameter value must be in the NOMS
        start_time cannot be a date before today - 7 days
    """
    if dataset == "aclImdb":
        make_dataset_aclImdb()
    elif dataset == "allocine":
        make_dataset_allocine(
            split)
    elif dataset == "twitter":
        download_tweets(txt, mention, start_time, end_time, tweet_fields)
        
# ########################################################################### #
#                                   Main                                      #
# ########################################################################### #
if __name__ == '__main__':
    pass
