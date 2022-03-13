#! /bin/bash -

PATH_DATASET_TRAIN="data/processed/allocine/train.csv"
PATH_DATASET_TEST="data/processed/allocine/test.csv"

if [ -f "$PATH_DATASET_TRAIN" ]
then
echo "Dataset train already exist"
else
    echo "Dataset do not exist yet lets make dataset !"
    poetry run python -m src data --download allocine --split train
fi


if [ -f "$PATH_DATASET_TEST" ]
then
echo "Dataset test already exist"
else
    echo "Dataset do not exist yet lets make dataset !"
    poetry run python -m src data --download allocine --split test
fi


poetry run python -m src models --model naive-bayes --train $PATH_DATASET_TRAIN --test $PATH_DATASET_TEST

poetry run pytest
