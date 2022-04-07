import argparse

from src.data.make_dataset.aclImdb import make_dataset_aclImdb
from src.data.make_dataset.allocine import make_dataset_allocine
from src.data.download.download_tweets import download_tweets

# ########################################################################### #
#                                 Constants                                   #
# ########################################################################### #
lst_candidats = ["Pecresse",
                 "Zemmour",
                 "Dupont-Aignan",
                 "Melenchon",
                 "Le Pen",
                 "Lassalle",
                 "Hidalgo",
                 "Macron",
                 "Jadot",
                 "Roussel",
                 "Arthaud",
                 "Poutou"]

# ########################################################################### #
#                                 Functions                                   #
# ########################################################################### #


def add_data_args(parser):
    # Specify to the data mentioning a specific candidats or aclImdb
    parser.add_argument('--download',
                        default='aclImdb',
                        choices=['twitter', 'aclImdb', "allocine"],
                        help="Download the specified dataset")

    # Specify to the data collector the split of the dataset
    parser.add_argument('--split',
                        default='train',
                        choices=['train', 'test', "validation"],
                        help="Download the specified dataset")

    # Specify to the data collector to download tweets mentionning this user
    parser.add_argument('--text',
                        default=None,
                        help="Download the tweets from this user")

    # Specify to the data collector to download tweets mentionning this user
    parser.add_argument('--mention',
                        choices=lst_candidats,
                        help="Download the tweets from this user")

    # Specify the date from which the tweets will be download
    parser.add_argument('--start_time',
                        default=None,
                        help="Download the tweets from this date")

    # Specify the date to which the tweets will be download
    parser.add_argument('--end_time',
                        default=None,
                        help="Download the tweets to this date")

    # Specify the tweet fields of the tweets will be download
    # for a lighter version of dataset, one can used: default='id,created_at,text',
    parser.add_argument('--tweet_fields',
                        default="author_id,created_at,id,public_metrics,text",
                        help="Specify the tweet fields")


def data_main(args):
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
    if args.download == "aclImdb":
        make_dataset_aclImdb()
    elif args.download == "allocine":
        make_dataset_allocine(
            args.split)
    elif args.download == "twitter":
        download_tweets(args.text,
                        args.mention,
                        args.start_time,
                        args.end_time,
                        args.tweet_fields)


# ########################################################################### #
#                                   Main                                      #
# ########################################################################### #
if __name__ == '__main__':
    pass
