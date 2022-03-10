import argparse
from src.data.main import data_main
from src.features.main import features_main
from src.models.main import models_main
from src.visualization.main import visualization_main

from omegaconf import OmegaConf
import hydra


# ########################################################################### #
#                                 Constants                                   #
# ########################################################################### #
lst_candidats = ["Pécresse",
                 "Zemmour",
                 "Dupont-Aignan",
                 "Mélenchon",
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
# @hydra.main(config_path="./configs", config_name="config")
# def accessing_hydra_config(cfg):
#     # Print the config file using `to_yaml` method which prints in a pretty manner
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
    help='Differentiate between data, features, models and visualizations commands',
    dest="subparser")

#####
# Sub parser concerning download of the data
######
parser_add = subparsers.add_parser('data', help='Data related commands')

# Specify to the data mentioning a specific candidats or aclImdb
parser_add.add_argument('--download',
                        default='aclImdb',
                        choices=['twitter', 'aclImdb'],
                        help="Download the specified dataset")

# Specify to the data collector to download tweets mentionning this text
parser_add.add_argument('--text',
                        choices=None,
                        help="Download the tweets containing this text")

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

#####
# Sub parser concerning ...
######
parser_features = subparsers.add_parser(
    'features', help='Features related commands')

#####
# Sub parser concerning the modelisation
######
parser_models = subparsers.add_parser(
    'models', help='Models related commands')

#####
# Sub parser concerning the visualization
######
parser_features = subparsers.add_parser(
    'visualization', help='Visualization related commands')


# Parsing args
args = parser.parse_args()
print(args)


if args.subparser == "data":
    data_main(args.download, args.text, args.mention, args.start_time, args.end_time)
elif args.subparser == "features":
    features_main()
elif args.subparser == "models":
    models_main()
elif args.subparser == "visualization":
    visualization_main()
