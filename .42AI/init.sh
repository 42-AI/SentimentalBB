#!/bin/sh

RED="\e[1;31m"
END="\e[0m"

echo $RED "INIT: " $END "Copy of hook commit..."
mkdir -p .git/hooks/
cp .42AI/pre-commit.git .git/hooks/pre-commit


echo $RED "INIT: " $END "Testing your python version..."
python .42AI/test_environment.py

echo $RED "INIT: " $END "Creating data directories..."
mkdir -p data/raw
mkdir -p data/processed
mkdir -p data/external
mkdir -p data/interim

echo $RED "INIT: " $END "Upgrading pip..."
pip install --upgrade pip

echo $RED "INIT: " $END "Installing python dependancies..."
pip install -r requirements.txt

# echo $RED "INIT: " $END "Downloading hello world dataset..."
# sh scripts/download_dataset.sh

echo $RED "INIT: " $END "Adding .envrc ..."
echo "source venv/bin/activate" > .envrc
