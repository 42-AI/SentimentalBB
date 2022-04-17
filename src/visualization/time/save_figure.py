import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

from src.visualization.time.prepare_results import get_candidate_all_days_predictions


def make_time_bars_figure(ax, candidate, df, relative=True):  # load dataset
    c_pos = sns.color_palette("pastel")[2]
    c_net = sns.color_palette("pastel")[7]
    c_neg = sns.color_palette("pastel")[3]

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
    # df['s_day'] = df['day'].astype(str)
    # df['s_day'] = df['s_day'].apply(lambda x: x[0] + "-" + x[1:])
    total_all = df.groupby('day')["preds_total"].sum().reset_index()
    # print(df)

    for dic in multi_plot:
        column = dic["column"]
        print(f"Taking care of {column}")
        color = dic["color"]

        total_1 = df.groupby('day')[[column]].sum().reset_index()

        if relative:
            new_col = column + "_percent"
            total_1[new_col] = total_1[column] / total_all["preds_total"]
            bar1 = sns.barplot(x="day",  y=new_col,
                               data=total_1, color=color, ax=ax)
        else:
            bar1 = sns.barplot(x="day",  y=column,
                               data=total_1, color=color, ax=ax)

        bar1.set_xticklabels(bar1.get_xticklabels(), rotation=45)
        # bar1.set_xticklabels(total_1["s_day"], rotation=45)

    top_bar = mpatches.Patch(color=c_pos, label='Positive')
    # mid_bar = mpatches.Patch(color=c_net, label='Neutral')
    bot_bar = mpatches.Patch(color=c_neg, label='Negative')
    ax.legend(handles=[top_bar, bot_bar])

    ax.set_xlabel("Month-Day")
    ax.set_ylabel("Sentiment")
    ax.set_title(candidate)


def save_figure_candidate(candidate, weights_in):
    df = get_candidate_all_days_predictions(candidate, weights_in)

    print("Generating figure...")
    sns.set_context(context="talk", font_scale=3, rc=None)
    plt.figure(figsize=(16 * 2, 9 * 2))
    ax = plt.gca()
    make_time_bars_figure(ax, candidate, df)
    fig_path = f"./reports/figures/bar_stacked_{candidate}.png"
    plt.savefig(fig_path)
    print("Done !")


def save_figure_candidate_duel(weights_in, candidate_1, candidate_2):
    df_1 = get_candidate_all_days_predictions(candidate_1, weights_in)
    df_2 = get_candidate_all_days_predictions(candidate_2, weights_in)

    sns.set_context(context="talk", font_scale=3, rc=None)
    f, axs = plt.subplots(2, 1, figsize=(16 * 2, 8 * 2 * 2))

    print("Generating figure...")
    make_time_bars_figure(axs[0], candidate_1, df_1)
    make_time_bars_figure(axs[1], candidate_2, df_2)
    f.tight_layout(pad=3.0)

    fig_path = f"./reports/figures/bar_stacked_{candidate_1}_{candidate_2}.png"
    plt.savefig(fig_path)

    print("Done !")
