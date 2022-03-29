import os
import sys
import shutil
from unittest.mock import NonCallableMagicMock
import yaml
import pandas as pd
import json

from click import MissingParameter
from searchtweets import gen_request_parameters, load_credentials, collect_results

from src.data.make_dataset.aclImdb import make_dataset_aclImdb
from src.data.make_dataset.allocine import make_dataset_allocine

# ########################################################################### #
#                                 Constants                                   #
# ########################################################################### #
EXPECTED_KEYS_CREDENTIALS = ['SEARCHTWEETS_ENDPOINT',
                             'SEARCHTWEETS_BEARER_TOKEN',
                             'SEARCHTWEETS_CONSUMER_KEY',
                             'SEARCHTWEETS_CONSUMER_SECRET']

CANDIDATS = ["Valérie Pécresse",
             "Eric Zemmour",
             "Nicolas Dupont-Aignan",
             "Jean-Luc Mélenchon",
             "Marine Le Pen",
             "Jean Lassalle",
             "Anne Hidalgo",
             "Emmanuel Macron",
             "Yannick Jadot",
             "Fabien Roussel",
             "Nathalie Arthaud",
             "Philippe Poutou"]

NOMS = ["Pecresse",
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
        "Poutou"]

TAGS = {"Pecresse": "@avecValerie",
        "Zemmour": "@ZemmourEric",
        "Dupont-Aignan": "@dupontaignan",
        "Melenchon": "@JLMelenchon",
        "Le Pen": "@MLP_officiel",
        "Lassalle": "@jeanlassalle",
        "Hidalgo": "@Anne_Hidalgo",
        "Macron": "@EmmanuelMacron",
        "Jadot": "@yjadot",
        "Roussel": "@AvecRoussel",
        "Arthaud": "@n_arthaud",
        "Poutou": "@PhilippePoutou"}

CREDENTIAL_FILE = f".twitter_keys.yaml"
# maybe later we would be able to use all, then we could change with search_tweets_v2_all
TWITTER_KEY = 'search_tweets_v2_recent'
NB_MAX_TWEETS = 50  # Max number of tweets one wants
RES_PER_CALL = 10  # Max number of tweets per query to Twitter API
CONFIG_YAML = ".config.yaml"
SAVE_PATH = "data/raw/twitter"
# ########################################################################### #
#                                 Functions                                   #
# ########################################################################### #


def dataset_to_csv(df_dataset: pd.DataFrame, filename: str):
    """ Saves the dataset into a file in the specified directory.
    Args:
    -----
        df_dataset [pandas DataFrame]: dataframe containing the dataset.
        filename [str]: name of the file where df will be saved.
    Return:
    -------
        None
    """
    csv_path = f"{SAVE_PATH}/{filename}.csv"
    print("dataset_to_csv ::: ", csv_path)
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    tmp_path = (f"{SAVE_PATH}/tmp")
    lst_files = os.listdir(tmp_path)
    df_dataset = None
    for tmp_file in lst_files:
        df_tmp = pd.read_csv(SAVE_PATH + "/tmp/" + tmp_file, index_col=False)
        if df_dataset is None:
            df_dataset = df_tmp
        else:
            df_dataset = pd.concat((df_dataset, df_tmp), ignore_index=True)
        print(df_dataset)
    #df_dataset.reset_index(inplace=True, drop=True)
    df_dataset.to_csv(csv_path)
    shutil.rmtree(SAVE_PATH + "/tmp/")


def chunk_to_csv(df_chunk: pd.DataFrame, mention: str,):
    """ Saves the temporary tweets chunk to a temporary csv file pior to fusion.
    This is to limit the lost of results in case the request or the saving of the dataset
    encounter an issue.
    Args:
    -----
        df_dataset [pandas DataFrame]: dataframe containing the dataset.
        mention [str]: mention of a candidat in the forged request.
    Return:
    -------
        None
    """
    print(df_chunk.columns)
    tmp_last_date = df_chunk['created_at'].iloc[0]
    tmp_first_date = df_chunk['created_at'].iloc[-1]
    tmp_last_id = df_chunk['id'].iloc[0]
    tmp_first_id = df_chunk['id'].iloc[-1]
    tmp_file = (f"{SAVE_PATH}/tmp/{mention.replace('@', '')}_start_time-"
                f"{tmp_first_date}_last_time-{tmp_last_date}_firstID-"
                f"{tmp_first_id}_lastID-{tmp_last_id}")
    os.makedirs(os.path.dirname(tmp_file), exist_ok=True)
    df_chunk.to_csv(tmp_file, index=False)


def metadata_to_json(metadata: dict, filename: str):
    """ Saves the meta data of the request into a file in the specified directory.
    Args:
    -----
        metadata [dictionary]: dictionary containing the metadata of the request.
        filename [str]: name of the file where df will be saved.
    Return:
    -------
        None
    """
    json_path = f"{SAVE_PATH}/{filename}.json"
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    dct_request = {}
    dct_request["query"] = metadata[0]
    for ii, meta in enumerate(metadata[1:]):
        dct_request[f"request {ii+1}"] = meta
    with open(json_path, 'w') as jsonfile:
        json.dump(dct_request, jsonfile, indent=4,
                  separators=(',', ': '), sort_keys=True)


def twiterAPI_credentials():
    """ Checking if the credentials are in the env, otherwise it tries to
    retrieve them from ".conf.yaml".
    The function expects to have 4 credentials:
        * SEARCHTWEETS_ENDPOINT,
        * SEARCHTWEETS_BEARER_TOKEN,
        * SEARCHTWEETS_CONSUMER_KEY,
        * SEARCHTWEETS_CONSUMER_SECRET.
    Args:
    -----
        No argument
    Return:
    -------
        None
    """
    # Checking the presence of the credentials in the env
    catched = False
    if any([k not in os.environ.keys() for k in EXPECTED_KEYS_CREDENTIALS]):
        s = ('Missing at least one Twitter API credentials.'
             'One expected to have SEARCHTWEETS_ENDPOINT, '
             'SEARCHTWEETS_BEARER_TOKEN, SEARCHTWEETS_CONSUMER_KEY'
             'SEARCHTWEETS_CONSUMER_SECRET')
        print(s, file=sys.stderr)
    else:
        # if the credentials are in the env it is fine
        catched = True
    if not catched:
        # if the credentials are not in the env we try to look into .conf.yaml
        # retrieve of the credentials from the file
        if os.path.exists(CONFIG_YAML):
            try:
                with open(CONFIG_YAML, 'r') as configfile:
                    twitter_credentials = yaml.safe_load(configfile)
                # Checking we retrieved all of them
                if any([k not in twitter_credentials.keys()
                        for k in EXPECTED_KEYS_CREDENTIALS]):
                    raise UserWarning
            except yaml.YAMLError as err:
                print(err, file=sys.stderr)
            except UserWarning:
                s = ("It seems there is at least one credentials missing.")
                print(s, file=sys.stderr)
            else:
                # If credentials are all catched, we add them in the env
                catched = True
                for key, val in twitter_credentials:
                    os.environ[key] = val
    # If the credentials are not found in env or in .config.yaml
    if not catched:
        s = ("You need to provide Twitter API credentials in your env "
             "or they should be present in a file 'config.yaml'.")
        raise EnvironmentError(s)


def transform_tweets(tweets):
    """ Return the tweets (collected via Twitter API method `collect_results`)
    in a form of a list.
    Args:
    -----
        tweets [List[Dict[...]]]: return of collect_results (API twitter method)
    Return:
    -------
        df_tweets [pandas DataFrame]: all the data about the tweets.
    """
    tweets_meta, tweets_data = tweets['meta'], tweets['data']  # for the moment metadata of the request are unused
    # Collecting the keys in data. For now only id and text but later with a better access we could have more keys
    lst_cols = list(tweets_data[0].keys())

    # Creating dictionary which will receive the data
    # Instead of having a list of dictionnaries we will have a dictionnary of lists
    dct_data_tweets = {}
    for k in lst_cols:
        dct_data_tweets[k] = []

    for ii in range(len(tweets_data)):
        for k in lst_cols:
            dct_data_tweets[k].append(tweets_data[ii][k])

    df_tweets = pd.DataFrame(dct_data_tweets)
    return df_tweets, tweets_meta


def make_dataset_twitter(txt: str, mention: str, start_time: str, end_time: str, tweet_fields: str = "id,created_at,text"):
    """ Handles the forging of the query a collect the request from twitter API.
    Args:
    -----
        txt [str]: text one wish to be present within the tweets.
        mention [str]: mention of a candidat in the forged request.
        start_time [str]: starting date from which tweets will be download.
        end_time [str]: ending date until which tweets will be download.
        tweet_fields[str]: specify the tweet fields. Defaults is 'id,created_at,text'.
    Return:
    -------
        tweets [List[Dict[...]]]: all the tweets collect from the request.
    Remarks:
    --------
        Concerning tweet_fields parameter, it must contain:
        attachments,author_id,context_annotations,conversation_id,created_at,
        entities,geo,id,in_reply_to_user_id, lang,non_public_metrics,organic_metrics,
        possibly_sensitive,promoted_metrics,public_metrics,referenced_tweets,
        reply_settings,source,text,withheld.
        Details can be found here: https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent
    """
    # Checking the argument mention:
    # if mention not in NOMS:
    # s = 'mention arguments must be within: ' + ' '.join(NOMS)
    # raise ValueError(s)
    # Checking the argument mention:
    # Testing the arguments start_time and end_time

    # Checking the start_time is before end_time:
    # Testing start_time < end_time

    # Checking the credentials and trying to retrieve them if necessary
    if not os.path.exists(CREDENTIAL_FILE):
        twiterAPI_credentials()
    search_args = load_credentials(filename=CREDENTIAL_FILE,
                                   yaml_key=TWITTER_KEY,
                                   env_overwrite=False)
    if mention is None:
        raise ValueError("One needs to mention a candidat.")
    s_query = mention
    if txt is not None:
        s_query += ' ' + txt
    s_query += ' ' + "-is:retweet -has:media"
    query = gen_request_parameters(s_query,
                                   results_per_call=RES_PER_CALL,
                                   granularity=None,
                                   start_time=start_time,
                                   end_time=end_time,
                                   tweet_fields=tweet_fields)

    df_tweets = None
    s = query
    json_acceptable_string = s.replace("'", "\"")
    d = json.loads(json_acceptable_string)
    print(query)
    metadata = [d]
    for chunk in collect_results(query, max_tweets=NB_MAX_TWEETS, result_stream_args=search_args):
        # transforming the chunk into a dataframe
        df_chunk, meta_chunk = transform_tweets(chunk)
        metadata.append(meta_chunk)
        # temporary save of the chunk, to avoid to lost the data in case there is an isuue
        chunk_to_csv(df_chunk, mention)

        if df_tweets is None:
            df_tweets = df_chunk
        else:
            df_tweets = pd.concat([df_tweets, df_chunk])
    return df_tweets, metadata


def data_main(dataset: str, split: str, txt: str, mention: str, start_time: str, end_time: str, tweet_fields: str):
    """ Main function to interact with the Twitter API or with aclImdb.
    It downloads and save the dataset/result into a file.
    Args:
    -----
        dataset [str]: type of dataset/API one wish to interact with.
        split[str]: specify the configuration (train or test)
        txt [str]: text one wish to be present within the tweets.
        mention [str]: mention of a candidat in the forged request.
        start_time [str]: starting date from which tweets will be download.
        end_time [str]: ending date until which tweets will be download.
        tweet_fields[str]: specify the tweet fields. Defaults is 'id,created_at,text'.
    Return:
    -------
        None
    Remarks:
    --------
        dataset parameter value must be in ['twitter', 'aclImdb', 'allocine']
        mention parameter value must be in the NOMS
        start_time cannot be a date before today - 7 days
    """
    if dataset == "aclImdb":
        make_dataset_aclImdb()
    elif dataset == "allocine":
        make_dataset_allocine(
            split)
    elif dataset == "twitter":
        df_data, tweets_metadata = make_dataset_twitter(txt,
                                                        TAGS[mention],
                                                        start_time,
                                                        end_time,
                                                        tweet_fields)
        df_data.reset_index(drop=True, inplace=True)
        last_date = df_data['created_at'].iloc[0]
        first_date = df_data['created_at'].iloc[-1]
        last_id = df_data['id'].iloc[0]
        first_id = df_data['id'].iloc[-1]
        filename = f"{mention.lower().replace(' ', '')}/{mention}_start_time-{first_date}_last_time-{last_date}_firstID-{first_id}_lastID-{last_id}"
        dataset_to_csv(df_data, filename)

        print(tweets_metadata)
        metadata_to_json(tweets_metadata, filename)


# ########################################################################### #
#                                   Main                                      #
# ########################################################################### #
if __name__ == '__main__':
    pass
