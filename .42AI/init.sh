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

PATH_PYTHON=`pwd`/venv/bin/python
PATH_ENVRC=`pwd`/.envrc

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
echo -e $COLOR_YELLOW "INIT:" $COLOR_RESET "Checking if .envrc exist"
if test -f "$PATH_ENVRC"; then
    echo -e $COLOR_GREEN "$PATH_ENVRC exists." $COLOR_RESET
else
    echo -e $COLOR_RED ".envrc do not exist at location $PATH_ENVRC" $COLOR_RESET
	echo "It can be created this way:"
	echo "$> echo \"source venv/bin/activate\" > .envrc"
	exit 1
fi


############################################################
# python version                                           #
############################################################
echo -e $COLOR_YELLOW "INIT: " $COLOR_RESET "Testing your python version..."
python .42AI/test_environment.py
if [ $? == 0 ]
then
    echo -e $COLOR_GREEN "Good python version" $COLOR_RESET
else
    echo -e $COLOR_RED "Bad python version" $COLOR_RESET
fi



############################################################
# git hook                                                 #
############################################################
echo -e $COLOR_YELLOW "INIT: " $COLOR_RESET "creating hook commit..."
mkdir -p .git/hooks/
cp .42AI/pre-commit.git .git/hooks/pre-commit

# echo $RED "INIT: " $END "Creating data directories..."
# mkdir -p data/raw
# mkdir -p data/processed
# mkdir -p data/external
# mkdir -p data/interim
# mkdir -p models

# echo $RED "INIT: " $END "Upgrading pip..."
# pip install --upgrade pip

# echo $RED "INIT: " $END "Installing python dependancies..."
# pip install -r requirements.txt

