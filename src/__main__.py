import argparse
from src.data.main import data_main
from src.features.main import features_main
from src.models.main import models_main, add_models_args
from src.visualization.main import visualization_main

from omegaconf import OmegaConf
import hydra


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

lst_models = ["random",
              "naive-bayes",
              "twitter-xlm-roberta-base-sentiment"]

# ########################################################################### #
#                                 Functions                                   #
# ########################################################################### #
# @hydra.main(config_path="./configs", config_name="config")
# def accessing_hydra_config(cfg):
#     # Print the config file using `to_yaml` method which prints in a
#       pretty manner
#     print(OmegaConf.to_yaml(cfg))
#     print(f"{cfg.training.max_epochs = }")


# ########################################################################### #
#                                    Main                                     #
# ########################################################################### #
# accessing_hydra_config()


# create the top-level parser
parser = argparse.ArgumentParser()

# Creation of subparsers Add and Deploy
subparsers = parser.add_subparsers(
    help='Differentiate between data, features, models and \
          visualizations commands',
    dest="subparser"
)

#####
# Sub parser concerning download of the data
######
parser_add = subparsers.add_parser('data', help='Data related commands')

# Specify to the data mentioning a specific candidats or aclImdb
parser_add.add_argument('--download',
                        default='aclImdb',
                        choices=['twitter', 'aclImdb', "allocine"],
                        help="Download the specified dataset")

# Specify to the data collector the split of the dataset
parser_add.add_argument('--split',
                        default='train',
                        choices=['train', 'test', "validation"],
                        help="Download the specified dataset")

# Specify to the data collector to download tweets mentionning this user
parser_add.add_argument('--text',
                        default=None,
                        help="Download the tweets from this user")

# Specify to the data collector to download tweets mentionning this user
parser_add.add_argument('--mention',
                        choices=lst_candidats,
                        help="Download the tweets from this user")

# Specify the date from which the tweets will be download
parser_add.add_argument('--start_time',
                        default=None,
                        help="Download the tweets from this date")

# Specify the date to which the tweets will be download
parser_add.add_argument('--end_time',
                        default=None,
                        help="Download the tweets to this date")

# Specify the tweet fields of the tweets will be download
# for a lighter version of dataset, one can used: default='id,created_at,text',
parser_add.add_argument('--tweet_fields',
                        default="author_id,created_at,id,public_metrics,text",
                        help="Specify the tweet fields")


#####
# Sub parser concerning the use of models to process existing data
######
parser_features = subparsers.add_parser(
    'features', help='Features related commands')
parser_features.add_argument('--data',
                             required=True,
                             help="Raw data set on which the model will\
                                 analyse sentiment",
                             )
parser_features.add_argument('--model',
                             help="Sentiment analysis based on the model entered",
                             default='twitter-xlm-roberta-base-sentiment',
                             choices=lst_models)

#####
# Sub parser concerning the modelisation
######
parser_models = subparsers.add_parser(
    'models', help='Models related commands')
add_models_args(parser_models)


#####
# Sub parser concerning the visualization
######
parser_visualization = subparsers.add_parser(
    'visualization', help='Visualization related commands')


# Parsing args
args = parser.parse_args()
print(args)


if args.subparser == "data":
    data_main(args.download, args.split, args.text, args.mention,
              args.start_time, args.end_time, args.tweet_fields)
elif args.subparser == "features":
    features_main(args.model, args.data)
elif args.subparser == "models":
    models_main(args)
elif args.subparser == "visualization":
    visualization_main()
