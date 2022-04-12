#! /bin/bash -

# Color related variables
COLOR_CYAN="\e[1;36m"
COLOR_PURPLE="\e[1;35m"
COLOR_RESET="\e[0m"

DD=("0315" "0316" "0318" "0319" "0320" "0321" "0322" "0323" "0328" "0329" "0330" "0331" "0401" "0402" "0403" "0404" "0405" "0406" "0407" "0408" "0409" "0410")
wheights="068_Naive_Bayes_04-12_11:01.z"

#if [ ! -d data/processed/twitter/predict/$DD ]; then
#	echo -e $COLOR_CYAN "Data of ${DD} is not processed. Processing..." $COLOR_RESET
#	poetry run python -m src data --task make-dataset --data twitter --split predict --candidate all --start_time 2022-$D2 --end_time 2022-$D2
#fi

for date in ${DD[@]}; do
	echo "Predict on data in data/processed/twitter/predict/${date}..."
	for filename in data/processed/twitter/predict/${date}/*.csv; do
		echo -e $COLOR_CYAN "processing..." "$filename" $COLOR_RESET
		poetry run python -m src models --task predict --model  naive-bayes --weights_in models/${wheights} --dataset_type predict --flat_y --in_csv ${filename}
	done
done

# poetry run dvc add data
# poetry run dvc push
# git add data.dvc
# git commit -m $1
# git push
