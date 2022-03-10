sh scripts/download_dataset.sh
python -m src data --download aclImdb
python -m src models --train data/processed/aclImdb/aclImdb_train.csv --test data/processed/aclImdb/aclImdb_test.csv --model "naive-bayes"