from click import MissingParameter
from src.data.make_dataset.aclImdb import make_dataset_aclImdb
from src.data.make_dataset.macron import make_dataset_macron
import os
import sys
import yaml
from searchtweets import gen_request_parameters, load_credentials, collect_results
# from searchtweets import ResultStream,

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

NOMS = ["Pécresse",
        "Zemmour",
        "Dupont-Aignan",
        "Mélenchon",
        "Le Pen",
        "Lassalle",
        "Hidalgo",
        "Macron",
        "Jadot",
        "Roussel",
        "Arthaud",
        "Poutou"]

TAGS = {"Pécresse": "@avecValerie",
        "Zemmour": "@ZemmourEric",
        "Dupont-Aignan": "@dupontaignan",
        "Mélenchon": "@JLMelenchon",
        "Le Pen": "@MLP_officiel",
        "Lassalle": "@jeanlassalle",
        "Hidalgo": "@Anne_Hidalgo",
        "Macron": "@EmmanuelMacron",
        "Jadot": "@yjadot",
        "Roussel": "@AvecRoussel",
        "Arthaud": "@n_arthaud",
        "Poutou": "@PhilippePoutou"}

CREDENTIAL_FILE = '.twitter_keys.yaml '
# maybe later we would be able to use all, then we could change with search_tweets_v2_all
TWITTER_KEY = 'search_tweets_v2_recent'
RES_PER_CALL = 40  # Max number of tweets per query to Twitter API
NB_MAX_TWWETS = 40  # Max number of tweets one wants
# ########################################################################### #
#                                 Functions                                   #
# ########################################################################### #


def twiterAPI_credentials():
    """ Checking if the credentials are in the env, otherwise it tries to
    retrieve them from ".conf.yaml".
    The function expects to have 4 credentials:
        * SEARCHTWEETS_ENDPOINT,
        * SEARCHTWEETS_BEARER_TOKEN,
        * SEARCHTWEETS_CONSUMER_KEY,
        * SEARCHTWEETS_CONSUMER_SECRET.
    Arguments:
    ----------
        No argument
    Return:
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
        try:
            # retrieve of the credentials from the file
            with open(".config.yaml", 'r') as configfile:
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


def data_main(dataset: str, txt: str, mention: str, start_time: str, end_time: str):
    """ Main function to interact with the Twitter API or with aclImdb.
    It downloads and save the dataset/result into a file.
    Args:
    -----
        dataset [str]: type of dataset/API one wish to interact with
        mention [str]: mention of a candidat in the forged request
        start_time [str]: starting date from which tweets will be download
        end_time [str]: ending date until which tweets will be download
    Return:
    -------
        None
    Remarks:
    --------
        dataset parameter value must be in ['twitter', 'aclImdb']
        mention parameter value must be in the NOMS
        start_time cannot be a date before today - 7 days
    """
    if dataset == "aclImdb":
        make_dataset_aclImdb()
    elif dataset == "twitter":
        # Checking the argument mention:
        if mention not in NOMS:
            s = 'mention arguments must be within: ' + ' '.join(NOMS)
            raise ValueError(s)
        # Checking the argument mention:
        # Testing the arguments start_time and end_time

        # Checking the start_time is before end_time:
        # Testing start_time < end_time

        # Checking the credentials and trying to retrieve them if necessary
        # twiterAPI_credentials()
        search_args = load_credentials(filename=CREDENTIAL_FILE,
                                       yaml_key=TWITTER_KEY,
                                       env_overwrite=False)
        if mention is None:
            raise ValueError("One needs to mention a candidat.")
        s_request = ""
        if txt is not None:
            s_request += txt + ' '
        if mention in NOMS:
            s_query += mention + ' '
        query = gen_request_parameters(s_query,
                                       results_per_call=RES_PER_CALL,
                                       granularity=None,
                                       start_time=start_time,
                                       end_time=end_time)
        tweets = collect_results(query,
                                 max_tweets=NB_MAX_TWWETS,
                                 result_stream_args=search_args)

        # make_dataset_macron()


# ########################################################################### #
#                                 Functions                                   #
# ########################################################################### #
if __name__ == '__main__':
    pass
