import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

from src.visualization.time.prepare_results import get_candidate_all_days_predictions


def make_and_save_figure(candidate, df, relative=True):  # load dataset
    c_pos = sns.color_palette("pastel")[2]
    c_net = sns.color_palette("pastel")[7]
    c_neg = sns.color_palette("pastel")[3]

    sns.set_context(context="talk", font_scale=3, rc=None)
    plt.figure(figsize=(16 * 2, 9 * 2))
    multi_plot = [
        {
            "column": "preds_total",
            "color": c_pos
        },
        {
            "column": "preds_not_positive",
            "color": c_net
        },
        {
            "column": "predict_Negative",
            "color": c_neg
        },
    ]

    for dic in multi_plot:
        column = dic["column"]
        color = dic["color"]
        total_1 = df.groupby('day')[column].sum().reset_index()
        bar1 = sns.barplot(x="day",  y=column, data=total_1, color=color)

    top_bar = mpatches.Patch(color=c_pos, label='Positive')
    mid_bar = mpatches.Patch(color=c_net, label='Neutral')
    bot_bar = mpatches.Patch(color=c_neg, label='Negative')
    plt.legend(handles=[top_bar, mid_bar, bot_bar])

    plt.xlabel("Month-Day")
    plt.ylabel("Sentiment")
    plt.title(candidate)

    fig_path = f"./reports/figures/bar_stacked_{candidate}.png"
    plt.savefig(fig_path)


def save_figure_candidate(candidate, weights_in):
    df = get_candidate_all_days_predictions(candidate, weights_in)

    print("Generating figure...")
    make_and_save_figure(candidate, df)
    print("Done !")
