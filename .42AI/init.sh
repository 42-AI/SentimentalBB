#! /bin/bash -

############################################################
# Default variables                                        #
############################################################
COLOR_RED="\e[1;31m"
COLOR_GREEN="\e[1;32m"
COLOR_YELLOW="\e[1;33m"
COLOR_BLUE="\e[1;34m"
COLOR_PURPLE="\e[1;35m"
COLOR_CYAN="\e[1;36m"
COLOR_RESET="\e[0m"

PATH_PYTHON=`type -a python3`
PATH_TWITTER_KEYS=`pwd`/.twitter_keys.yaml

############################################################
# Help                                                     #
############################################################
Help()
{
   # Display Help
   echo "Script to execute after the git clone of the project"
   echo "IT MUST BE LAUNCHED FROM THE PROJECT TOP DIRECTORY"
   echo
   echo "usage: bash .42AI/init.sh [--help] [python_path]" 
   echo "options:"
   echo "	--help          Print this Help."
   echo "   python_path     Optional path to python interpreter."
   echo "                   Defaults to: $PATH_PYTHON"
   echo
}

############################################################
############################################################
# Main program                                             #
############################################################
############################################################


############################################################
# Process the input options. Add options as needed.        #
############################################################
while test $# -gt 0
do
    case "$1" in
        --help) # Display Help
			Help
			exit 0
            ;;
        --*) # Bad option used
			echo "bad option $1"
			echo
			Help
			exit 1
            ;;
        *) # Setting up python path
			PYTHON_PATH=$1
			echo "Python path for this script has been set to: $PATH_PYTHON"
            ;;
    esac
    shift
done


############################################################
# .envrc                                                   #
############################################################
echo -e $COLOR_YELLOW "INIT:" $COLOR_RESET "Checking if .twitter_keys.yaml exist"
if test -f "$PATH_TWITTER_KEYS"; then
    echo -e $COLOR_GREEN "$PATH_TWITTER_KEYS exists." $COLOR_RESET
else
    echo -e $COLOR_RED "ERROR: .twitter_keys.yaml does not exist at location $PATH_TWITTER_KEYS" $COLOR_RESET
	echo "It can be created this way:"
 	echo "$> echo \"<name_of_key:\n
  	endpoint: <URL_OF_ENDPOINT>\n
  	bearer_token: <YOUR_BEARER_TOKEN>\n
  	consumer_key: <YOUR_CONSUMER_KEY>\n
  	consumer_secret: <YOUR_CONSUMER_SECRET>\" > .twitter_keys.yaml"
 	exit 1
fi


############################################################
# python version                                           #
############################################################
echo -e $COLOR_YELLOW "INIT: " $COLOR_RESET "Testing your python version..."
# poetry env use $PATH_PYTHON
if poetry run python .42AI/test_environment.py;
then
    echo -e $COLOR_GREEN "Good python version" $COLOR_RESET
else
    echo -e $COLOR_RED "ERROR: Bad python version" $COLOR_RESET
	exit 1
fi


############################################################
# git hook                                                 #
############################################################
echo -e $COLOR_YELLOW "INIT: " $COLOR_RESET "Creating hook commit..."
mkdir -p .git/hooks/
cp .42AI/pre-commit.git .git/hooks/pre-commit


############################################################
# Creating directories                                     #
############################################################
echo -e $COLOR_YELLOW "INIT: " $COLOR_RESET "Creating data directories..."
mkdir -p data/raw
mkdir -p data/processed
mkdir -p data/external
mkdir -p data/interim

echo -e $COLOR_YELLOW "INIT: " $COLOR_RESET "Creating models directory..."
mkdir -p models


############################################################
# Installing dependencies                                  #
############################################################
echo -e $COLOR_YELLOW "INIT: " $COLOR_RESET "Installing python dependancies..."
poetry install


############################################################
# aws cli                                                  #
############################################################

echo -e $COLOR_YELLOW "INIT: " $COLOR_RESET "Verifying if aws cli is installed"
if aws --version;
then
    echo -e $COLOR_GREEN "aws is installed !" $COLOR_RESET
else
    echo -e $COLOR_RED "ERROR: aws is not installed, please follow the steps in Setup.md" $COLOR_RESET
fi


echo -e $COLOR_YELLOW "INIT: " $COLOR_RESET "Verifying that aws cli is configured"
if [[ $(aws configure get aws_access_key_id) ]]; then
    echo -e $COLOR_GREEN "aws is configured !" $COLOR_RESET
else
    echo -e $COLOR_RED "ERROR: aws is not configured, please run \`aws configure\`" $COLOR_RESET
fi


############################################################
# DVC                                                      #
############################################################



echo -e $COLOR_YELLOW "INIT: " $COLOR_RESET "Verifying that DVC remote is setup"
if [[ $(poetry run dvc remote list | grep s3-remote) ]]; then
    echo -e $COLOR_GREEN "DVC remote is already setup!" $COLOR_RESET
else
	echo "DVC remote is not yet setup"
	echo -e $COLOR_YELLOW "INIT: " $COLOR_RESET "Seting up DVC remote"
	poetry run dvc remote add -f s3-remote s3://lab-presidentials/storage
fi


echo -e $COLOR_YELLOW "INIT: " $COLOR_RESET "Pulling DVC data !"
poetry run dvc pull -r s3-remote

echo -e $COLOR_GREEN "PROJECT IS FULLY INITIALIZED <3" $COLOR_RESET
