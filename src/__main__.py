import argparse
from omegaconf import OmegaConf
import hydra

from src.data.main import data_main, add_data_args
from src.features.main import features_main
from src.models.main import models_main, add_models_args
from src.visualization.main import visualization_main

# ########################################################################### #
#                                 Constants                                   #
# ########################################################################### #
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
subparsers = parser.add_subparsers(
    help='Differentiate between data, features, models and \
          visualizations commands',
    dest="subparser"
)

#####
# Sub parser concerning download of the data
######
parser_data = subparsers.add_parser('data', help='Data related commands')
add_data_args(parser_data)


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
    data_main(args)
elif args.subparser == "features":
    features_main(args.model, args.data)
elif args.subparser == "models":
    models_main(args)
elif args.subparser == "visualization":
    visualization_main()
