#! /bin/bash -

# Color related variables
COLOR_CYAN="\e[1;36m"
COLOR_PURPLE="\e[1;35m"
COLOR_RESET="\e[0m"

DD="0410"
D2="04-10"
candidates=("macron" "lepen")

if [ ! -d data/processed/twitter/predict/$DD ]; then
	echo -e $COLOR_CYAN "Data of ${DD} is not processed. Processing..." $COLOR_RESET
	poetry run python -m src data --task make-dataset --data twitter --split predict --candidate all --start_time 2022-$D2 --end_time 2022-$D2
fi

echo "Predict on data in data/processed/twitter/predict/$DD..."
for candidate in "${candidates[@]}"; do
	for filename in data/processed/twitter/predict/${DD}/${candidate}*.csv; do
		echo -e $COLOR_CYAN "processing..." "$filename" $COLOR_RESET
		poetry run python -m src models --task predict --model  huggingface --dataset_type predict --flat_y --in_csv ${filename}
	done
done

# poetry run dvc add data
# poetry run dvc push
# git add data.dvc
# git commit -m $1
# git push
