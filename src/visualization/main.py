from src.visualization.time.save_figure import save_figure_candidate

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


def add_visaulization_args(parser):
    # Specify on which data to perform the task
    parser.add_argument('--visu',
                        required=True,
                        default='time',
                        choices=['time'],
                        help="Type of visu")

    # Specify to the data collector the split of the dataset
    parser.add_argument('--candidate',
                        default=lst_candidats[0],
                        choices=lst_candidats,
                        help="candidate")


def visualization_main(args):
    if args.visu == "time":
        save_figure_candidate(args.candidate)
