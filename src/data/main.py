import argparse
from email.policy import default

from src.data.make_dataset.aclImdb import make_dataset_aclImdb
from src.data.make_dataset.allocine import make_dataset_allocine
from src.data.download.download_tweets import download_tweets
from src.data.make_dataset.make_dataset_twitter import make_dataset_twitter

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
                 "Poutou",
                 "all"]


# ########################################################################### #
#                                 Functions                                   #
# ########################################################################### #


def add_data_args(parser):
    # Specify which task to perform: download, make_dataset or load
    parser.add_argument('--task',
                        required=True,
                        choices=['download', 'make-dataset', 'load-dataset'],
                        help="Specify which task to perform.")

    # Specify on which data to perform the task
    parser.add_argument('--data',
                        default='aclImdb',
                        choices=['twitter', 'aclImdb', "allocine"],
                        help="Specify which type of data on which the task\
                             will be performed")

    # Specify to the data collector the split of the dataset
    parser.add_argument('--split',
                        default=None,
                        choices=['train', 'test', "validation", 'predict'],
                        help="For make_dataset: specify the action the \
                             dataset will be used for ")

    # Download twitter: specify user
    parser.add_argument('--user',
                        default=None,
                        help="Only for download tweets: Download the tweets\
                             from this user")

    # Candidate Mention
    parser.add_argument('--candidate',
                        default=None,
                        choices=lst_candidats,
                        help="Download the tweets mentioning this candidate")

    # Start Time
    parser.add_argument('--start_time',
                        default=None,
                        help="""Task to be performed on tweets from date:
                             Format for make_dataset: 'yyyy-mm-dd'
                             Format for download: 'yyyy-mm-dd hh:mm'
                             Required for twitter""")

    # End Time
    parser.add_argument('--end_time',
                        default=None,
                        help="""Task to be performed on tweets up to date:
                             Format for make_dataset: 'yyyy-mm-dd'
                             Format for download: 'yyyy-mm-dd hh:mm'
                             Required for twitter""")

    # Twitter Dowload: Tweet fields
    # for a lighter dataset, one can used: default='id,created_at,text',
    parser.add_argument('--tweet_fields',
                        default="author_id,created_at,id,public_metrics,text",
                        help="Dowload Twitter: Specify the tweet fields")


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
    if args.task == 'download':
        if args.data == "aclImdb":
            make_dataset_aclImdb()
        elif args.data == "allocine":
            make_dataset_allocine(
                args.split)
        elif args.data == "twitter":
            download_tweets(args.user,
                            args.candidate,
                            args.start_time,
                            args.end_time,
                            args.tweet_fields)
    elif args.task == 'make-dataset':
        if args.data == 'twitter':
            make_dataset_twitter(args)



# ########################################################################### #
#                                   Main                                      #
# ########################################################################### #
if __name__ == '__main__':
    pass
