import argparse
from email.policy import default

from src.data.download.download_tweets import download_tweets
from src.data.make_dataset.make_dataset_twitter import make_dataset_twitter
from src.data.make_dataset.make_dataset_allocine import make_dataset_allocine
from src import config

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
                        required=True,
                        default=None,
                        choices=['twitter', 'aclImdb', "allocine"],
                        help="Specify which type of data on which the task\
                             will be performed")

    # Specify to the data collector the split of the dataset
    parser.add_argument('--split',
                        default=None,
                        choices=['train', 'test', "validation", 'predict'],
                        help="Required For make_dataset: specify the action the \
                             dataset will be used for ")

    # Download twitter: specify user
    parser.add_argument('--text',
                        default=None,
                        help="Only for download tweets: Download the tweets\
                             containing this text")

    # Candidate Mention
    parser.add_argument('--candidate',
                        default=None,
                        help="""For twitter download or twitter make-dataset: \
                        predictDownload the tweets mentioning \
                        this candidate""")

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
                        help="""Task to be performed on tweets up to date:\n
                             Format for make_dataset: 'yyyy-mm-dd'\n
                             Format for download: 'yyyy-mm-dd hh:mm'\n
                             Required for twitter""")

    # Twitter Dowload: Tweet fields
    # for a lighter dataset, one can used: default='id,created_at,text',
    parser.add_argument('--tweet_fields',
                        default="author_id,created_at,id,public_metrics,text,lang",
                        help="Dowload Twitter: Specify the tweet fields")

    # Make test set twitter: nb of tweets
    parser.add_argument('--nb_tweets',
                        default=120,
                        help="For make-dataset twitter test: \
                            nb of tweets to select for test set. \
                            Range should be [12-480].")

    # Make test set twitter: nb of tweets
    parser.add_argument('--nb_reviews',
                        default=180,
                        help="For make-dataset allocine test: \
                            nb of reviews to select for test set. \
                            Range should be [1-10000].")

    # Make test set twitter: csv in
    parser.add_argument('--csv_in',
                        default=None,
                        help="csv to choose tweets from in order to make test set, \
                                path relative to data/processed/twitter/predict.")

    # Make test set twitter: label tweets
    parser.add_argument('--label',
                        default=False,
                        action="store_true",
                        help="For labeling tweets.")


def data_main(args):
    if args.task == 'download':
        if args.data == "aclImdb":
            make_dataset_aclImdb()
        elif args.data == "allocine":
            make_dataset_allocine(
                args.split)
        elif args.data == "twitter":
            download_tweets(args.text,
                            args.candidate,
                            args.start_time,
                            args.end_time,
                            args.tweet_fields)
    elif args.task == 'make-dataset':
        if args.data == 'twitter':
            make_dataset_twitter(args)
        elif args.data == 'allocine':
            make_dataset_allocine(args)


# ########################################################################### #
#                                   Main                                      #
# ########################################################################### #
if __name__ == '__main__':
    pass
