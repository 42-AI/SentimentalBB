import os
import sys
import yaml
import pandas as pd

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
NB_MAX_TWEETS = 40  # Max number of tweets one wants
RES_PER_CALL = NB_MAX_TWEETS  # Max number of tweets per query to Twitter API
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
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df_dataset.to_csv(csv_path)


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
    _, tweets_data = tweets[0]['meta'], tweets[0]['data']  # for the moment metadata of the request are unused
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

    return df_tweets


def make_dataset_twitter(txt: str, mention: str, start_time: str, end_time: str):
    """ Handles the forging of the query a collect the request from twitter API.
    Args:
    -----
        txt [str]: text one wish to be present within the tweets.
        mention [str]: mention of a candidat in the forged request.
        start_time [str]: starting date from which tweets will be download.
        end_time [str]: ending date until which tweets will be download.
    Return:
    -------
        tweets [List[Dict[...]]]: all the tweets collect from the request.
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
    s_query = ""
    if txt is not None:
        s_query += txt + ' '
    s_query += mention + ' '
    query = gen_request_parameters(s_query,
                                   results_per_call=RES_PER_CALL,
                                   granularity=None,
                                   start_time=start_time,
                                   end_time=end_time)
    tweets = collect_results(query,
                             max_tweets=NB_MAX_TWEETS,
                             result_stream_args=search_args)
    tweets = transform_tweets(tweets)
    print(tweets)
    return tweets


def data_main(dataset: str, split: str, txt: str, mention: str, start_time: str, end_time: str):
    """ Main function to interact with the Twitter API or with aclImdb.
    It downloads and save the dataset/result into a file.
    Args:
    -----
        dataset [str]: type of dataset/API one wish to interact with.
        txt [str]: text one wish to be present within the tweets.
        mention [str]: mention of a candidat in the forged request.
        start_time [str]: starting date from which tweets will be download.
        end_time [str]: ending date until which tweets will be download.
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
        df_data = make_dataset_twitter(
            txt, TAGS[mention], start_time, end_time)

        filename = f"{mention.lower().replace(' ', '')}/{dataset}_{mention}_{start_time}_{end_time}"
        dataset_to_csv(df_data, filename)


# ########################################################################### #
#                                   Main                                      #
# ########################################################################### #
if __name__ == '__main__':
    pass
