poetry run python -m src data --download allocine --split train
poetry run python -m src data --download allocine --split test
poetry run python -m src models --model naive-bayes --train data/processed/allocine/train.csv --test data/processed/allocine/test.csv
poetry run pytest
