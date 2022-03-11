bash scripts/download_dataset.sh

PATH_DATASET_TRAIN="data/processed/aclImdb/aclImdb_test.csv"

if [ -f "$PATH_DATASET_TRAIN" ]
then
echo "Dataset already exist, lets train !"
else
    echo "Dataset do not exist yet lets make dataset !"
    python -m src data --download aclImdb
fi



python -m src models --train data/processed/aclImdb/aclImdb_train.csv --test data/processed/aclImdb/aclImdb_test.csv --model "naive-bayes"