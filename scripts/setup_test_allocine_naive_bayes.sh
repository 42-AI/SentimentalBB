
PATH_DATASET_TRAIN="data/processed/allocine/train.csv"
PATH_DATASET_TEST="data/processed/allocine/test.csv"

if [ -f "$PATH_DATASET_TRAIN" ]
then
echo "Dataset already exist, lets train !"
else
    echo "Dataset do not exist yet lets make dataset !"
    poetry run python -m src data --download allocine --split train
fi


if [ -f "$PATH_DATASET_TRAIN" ]
then
echo "Dataset already exist, lets train !"
else
    echo "Dataset do not exist yet lets make dataset !"
    poetry run python -m src data --download allocine --split test
fi


poetry run python -m src models --model naive-bayes --train data/processed/allocine/train.csv --test data/processed/allocine/test.csv

poetry run pytest
