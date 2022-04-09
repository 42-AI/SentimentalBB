#! /bin/bash -

# poetry run python3.8 -m src visualization --visu time --candidate "all"

rm -f docs/index.md
cp README.md docs/index.md

rm -rf docs/reports
cp -r reports docs/reports
