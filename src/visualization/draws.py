import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os


def draw_pie_1(lst_candidats, filespath):
    """ Draw a pie with the mean of the Like/neutral/dislike ratio encoded
    into a color (blue = strongly positive / red = strongly negative) for
    each candidat.
    Args:
    -----
        lst_candidats [list]: ...
        filespath [str]: ...
    Return:
    -------
        None
    """
    lst_files = os.listdir(filespath)
    dct_res = {c: 0 for c in lst_candidats}
    # Calculs score en prenant en compte positif, neutre et negatif
    for f in lst_files:
        df = pd.open_csv(f)
        candidat = lst_files.split('_')[0]
        nb_positive = df['positive'].sum()
        nb_neutral = df['neutral'].sum()
        nb_negative = df['negative'].sum()
        tot = nb_positive + nb_neutral + nb_negative
        dct_res[candidat] = (1 * nb_positive + 0 *
                             nb_neutral - 1 * nb_negative) / tot
        # define Seaborn color palette to use

    palette = sns.color_palette("coolwarm", as_cmap=True)

    # create pie chart
    lst_c, lst_val = list(dct_res.keys()), list(dct_res.values())
    plt.pie(lst_val, labels=lst_c, colors=palette, autopct='%.0f%%')
    plt.colorbar(label="Like/Dislike Ratio", orientation="horizontal")
    plt.show()
    # date = lst_files.split('_')[1]
    # figname = f'pie_1_candidat_all_{date}.png'
    # plt.print_figure("reports/figures/" + figname)


def draw_pie_12(lst_candidats, filespath):
    """ Draw a pie with the mean of the Like/neutral/dislike ratio encoded
    into a color (blue = strongly positive / red = strongly negative) for
    each candidat.
    Args:
    -----
        lst_candidats [list]: ...
        filespath [str]: ...
    Return:
    -------
        None
    """
    lst_files = os.listdir(filespath)

    fig, axes = plt.subplots(3, 4, figsize=(26, 18))

    for ii, f in enumerate(lst_files):
        df = pd.open_csv(f)
        candidat = lst_files.split('_')[0]
        nb_positive = df['positive'].sum()
        nb_neutral = df['neutral'].sum()
        nb_negative = df['negative'].sum()
        data = [nb_positive, nb_neutral, nb_negative]
        labels = ['Positive', 'Neutral', 'Negative']
        axes[ii // 3][ii % 4].pie(data, labels, color=['#6789ed',
                                  '#3ebe3e1', '#d44f37'], autopct='%.0f%%')
        axes[ii // 3][ii % 4].set_title(candidat)

    plt.colorbar(label="Like/Dislike Ratio", orientation="horizontal")
    plt.show()
    # date = lst_files.split('_')[1]
    # figname = f'pie_12_candidat_each_{date}.png'
    # plt.print_figure("reports/figures/" + figname)
