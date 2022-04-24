from pytorch_lightning import Trainer
from src.models.pytorch.TweetLitModule import TweetLitModule
from src.data.load_dataset.TwitterDataModule import TwitterDataModule
from src.models.huggingface.roberta import HuggingFaceModel
from src.models.sklearn.Naive_Bayes import Naive_Bayes
from src.models.random.predict_model_random import RandomModel
import argparse

from src.models.ModelManager import ModelManager


def add_models_args(parser):
    parser.add_argument('--model',
                        help="Training based on the model entered",
                        default='random',
                        choices=['random', 'naive-bayes',
                                 'huggingface', 'torch']
                        )
    parser.add_argument('--task',
                        required=True,
                        help="Task to be perforemed",
                        choices=['train', 'test', 'predict']
                        )
    parser.add_argument('--dataset_type',
                        default="bi",
                        choices=['bi', 'tri', 'predict'],
                        help="Wether the dataset has 2 or 3 label",
                        )
    parser.add_argument('--flat_y',
                        default=False,
                        action="store_true",
                        help="Wether the dataset has 2 or 3 label",
                        )
    parser.add_argument('--in_csv',
                        required=True,
                        help="The input csv",
                        # type=argparse.FileType('r')
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
    if args.model == "torch":
        trainer = Trainer(max_epochs=10, accelerator='gpu', devices=1)

        csv_test = "src/tests/test_set_240tweets_labeled_0410.csv"
        csv_train = "data/processed/allocine/allocine_trainset_160000reviews.csv"
        # args.in_csv
        dm = TwitterDataModule(csv_test_path=csv_test,
                               csv_train_path=csv_train)

        model = TweetLitModule()

        trainer.fit(model=model, datamodule=dm)
        _ = trainer.test(model, datamodule=dm)

    else:
        if args.model == "naive-bayes":
            mdl = Naive_Bayes()
        elif args.model == "huggingface":
            mdl = HuggingFaceModel()
        elif args.model == "random":
            mdl = RandomModel()

        mm = ModelManager(mdl, args.dataset_type, args.flat_y)

        if args.weights_in:
            mm.load(args.weights_in)

        if args.task == "test":
            mm.test(args.in_csv, args.score)
        elif args.task == "train":
            mm.train(args.in_csv, args.weights_out)
        elif args.task == "predict":
            mm.predict(args.in_csv, args.out_csv)
