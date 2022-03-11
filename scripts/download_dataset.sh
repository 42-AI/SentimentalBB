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

PATH_DATASET=`pwd`/data/raw/StandfordSentiments/aclImdb


if [ -d $PATH_DATASET ]
then
    echo -e $COLOR_GREEN "Dataset is already downloaded!" $COLOR_RESET
    exit 0
else
    echo -e $COLOR_YELLOW "We will download the dataset" $COLOR_RESET
fi


wget http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz

mkdir -p $PATH_DATASET

mv aclImdb_v1.tar.gz $PATH_DATASET

tar -zxvf $PATH_DATASET/aclImdb_v1.tar.gz -C $PATH_DATASET >/dev/null

echo -e $COLOR_GREEN "Dataset downloaded !" $COLOR_RESET
