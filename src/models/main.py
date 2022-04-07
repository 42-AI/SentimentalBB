from src.models.sklearn.Naive_Bayes import naive_bayes_main
from src.models.huggingface.twitter_xlm_roberta_base_sentiment \
    import huggingface_predict, huggingface_main
import pandas as pd
import argparse


def add_models_args(parser):
    parser.add_argument('--model',
                        help="Training based on the model entered",
                        default='random',
                        choices=['random', 'naive-bayes', 'hugging-face']
                        )
    parser.add_argument('--task',
                        required=True,
                        help="Task to be perforemed",
                        choices=['train', 'test', 'predict']
                        )
    parser.add_argument('--train_csv',
                        # required=True,
                        help="Train set on which the model will be trained.\
							  Only if --task entered is train.\
							  Must be formatted like this:\
							  Column1: title:text format:str\
							  Column2: title:Positive format:[0/1]\
							  Column3: title:Negative format:[0/1]\
							  Column4: title:Neutral format:[0/1]",
                        type=argparse.FileType('r')
                        )
    parser.add_argument('--test_csv',
                        # required=True,
                        help="Train set on which the model will be tested.\
							  Only if --task entered is test.\
							  Must be formatted like this:\
							  Column1: title:text format:str\
							  Column2: title:Positive format:[0/1]\
							  Column3: title:Negative format:[0/1]\
							  Column4: title:Neutral format:[0/1]",
                        type=argparse.FileType('r')
                        )
    parser.add_argument('--predict_csv',
                        # required=True,
                        help="Train set on which the model will predict.\
							  Only if --task entered is predict.\
							  Must be formatted like this:\
							  Column1: title:text format:str",
                        type=argparse.FileType('r')
                        )
    parser.add_argument('--out_csv',
                        help="Path of output csv file: must finish by '.csv'\
							  Required if --task is test or predict"
                        )
    parser.add_argument('--weights_in',
                        help="Only if --task is test or predict.\
							  If no weights are passed and --task is test, \
							  the model will train first on the test_file.csv",
                        default=None
                        )
    parser.add_argument('--weights_out',
                        help="Path to save the weights if --task is train",
                        default=None
                        )
    parser.add_argument('--score',
                        help="Path to save the weights if --task is train",
                        choices=['accuracy'],
                        default='accuracy'
                        )


def models_main(args):
    """Redirect args to the asking model in the CLI

    Args:
            args: args passed in CLI
    """
    if args.model == "naive-bayes":
        naive_bayes_main(args)
    elif args.model == "hugging-face":
        huggingface_main(args)
        # if args.task == 'predict':
        #     huggin_face_predict(args.predict_csv, args.out_csv)
    else:
        print("Other models than Naive-Bayes or hugging-face not implemented \
			  yet")
