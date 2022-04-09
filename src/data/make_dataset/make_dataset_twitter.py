import pandas as pd
import re
import os
import sys
from datetime import datetime
from datetime import timedelta
from src import config


def make_dataset_predict(candidate: str, day: str):
    FOLDER_PATH = f"./data/raw/twitter/{candidate.lower().replace(' ', '')}"
    DATE = f'start_time-{day}'
    # Create a tmp df with all the csvs for candidate at day concatenated
    files = os.listdir(FOLDER_PATH)
    nb = 1
    list_dfs = []
    for file in files:
        if file.endswith(".csv") and DATE in file:
            list_dfs.append(pd.read_csv(FOLDER_PATH + '/' + file, index_col=0))
    if not list_dfs:
        print(f"No raw twitter csv for {candidate} at {day}")
        return
    df_tmp = pd.concat(list_dfs, axis=0, ignore_index=True)
    # Create good df with appropriate columns
    df_tmp['candidate'] = candidate
    df = df_tmp[['candidate']].copy()
    df['time'] = df_tmp['created_at'].\
        map(lambda x: re.search(r'\d{2}:\d{2}:\d{2}', x).group())
    df['tweet_id'] = df_tmp['id']
    df['text'] = df_tmp['text']
    # Suppress Retweets
    df = df[~df.text.str.contains("RT")]
    # Reset row indexes after suppression of RTs
    df = df.reset_index()
    df = df.drop('index', axis=1)
    # Export to csv
    new_date = datetime.strptime(day, '%Y-%m-%d').strftime('%m%d')
    PATH_TO_CSV = './data/processed/twitter/predict/' + new_date
    os.makedirs(PATH_TO_CSV, exist_ok=True)
    df.to_csv(f"{PATH_TO_CSV}/{candidate.lower().replace(' ', '')}"
              f"_{new_date}_{len(df)}tweets.csv")
    print(f"Csv created at {PATH_TO_CSV}/{candidate.lower().replace(' ', '')}"
          f"_{new_date}_{len(df)}tweets.csv")


def make_datasets_predict(args):
    # create datetime objects to loop over dates
    delta = timedelta(days=1)
    start_date = datetime.strptime(args.start_time, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_time, "%Y-%m-%d")
    # loop over dates and over candidates if "all"
    while (start_date <= end_date):
        if args.candidate == 'all':
            for candidate in config.lst_candidats:
                make_dataset_predict(candidate,
                                     start_date.strftime('%Y-%m-%d'))
        else:
            make_dataset_predict(args.candidate,
                                 start_date.strftime('%Y-%m-%d'))
        start_date += delta


def make_dataset_twitter(args):
    # Check for parsing errors
    if args.candidate is None or args.split is None or \
       args.start_time is None or args.end_time is None:
        print("You forgot at least one of the following arguments:\n"
              "-candidate\n"
              "-split\n"
              "-start_time\n"
              "-end_time")
        sys.exit()
    pattern = re.compile('2022-\d{2}-\d{2}')
    if not pattern.match(args.start_time) or \
       not pattern.match(args.end_time):
        print("start_time or end_time not formatted as 'yyyy-mm-dd'")
        sys.exit()
    # Dispatch between train, predict, test
    if args.split == 'predict':
        make_datasets_predict(args)
    else:
        print("Only predict has been coded yet for make_dataset twitter")
