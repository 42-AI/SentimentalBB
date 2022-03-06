import searchtweets
from searchtweets import ResultStream, gen_request_parameters, load_credentials
from searchtweets import collect_results
import pandas as pd
import os

user = "macron"
MAX_TWEET = 100
SAVE_PATH = f"data/raw/twitter/{user}/"


def make_dataset_macron():
    # Usage can be found here:
    #   https://github.com/twitterdev/search-tweets-python/blob/46386e0316b79096b5c5369abbc4f361b8153622/searchtweets/credentials.py#L114
    search_args = load_credentials(env_overwrite=False)
    query = gen_request_parameters(
        "Emmanuel Macron", results_per_call=100, granularity=None)
    print(query)
    tweets = collect_results(query, max_tweets=MAX_TWEET,
                             result_stream_args=search_args)

    def func(tweets, tweet_nb): return tweets[0]['data'][tweet_nb]['text']

    tweet_list = [func(tweets, i) for i in range(MAX_TWEET)]

    pre_df = {
        "text": tweet_list,
    }

    df = pd.DataFrame.from_dict(pre_df)
    csv_path = f"{SAVE_PATH}first_list.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df.to_csv(csv_path)
