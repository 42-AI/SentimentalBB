from numpy import require
from requests import request
from src.visualization.time.save_figure import save_figure_candidate
from src import config


def add_visaulization_args(parser):
    # Specify on which data to perform the task
    parser.add_argument('--visu',
                        required=True,
                        default='time',
                        choices=['time'],
                        help="Type of visu")

    # Specify to the data collector the split of the dataset
    parser.add_argument('--candidate',
                        default="all",
                        choices=config.lst_candidats_file_name + ["all"],
                        help="candidate")
    parser.add_argument('--weights_in',
                        required=True,
                        help="Model weights")


def visualization_main(args):
    if args.visu == "time":
        if args.candidate == "all":
            for candidate in config.lst_candidats_file_name:
                save_figure_candidate(candidate, args.weights_in)
        else:
            save_figure_candidate(args.candidate, args.weights_in)
