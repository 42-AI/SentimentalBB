#! /bin/bash -

# Color related variables
COLOR_CYAN="\e[1;36m"
COLOR_PURPLE="\e[1;35m"
COLOR_RESET="\e[0m"

# request forging Twitter API related variables
LEPEN=("#Marine2022" "#MarinePresidenteDeTousLesFrancais" "#JeVoteMarine" "#MacronDehors" "#McKingseyGate" "#MarinePresidente" "#Arrogant" "#MarinePresidente2022" "#mackinsey" "#TousSaufMacron" "#marine2022")
MACRON=("#NiMarineNiLePen" "#Macron2022" "#JeVoteMacron" "#JeVoteMacronAuDeuxiemeTour")
DD="04-25"
DATE_STARTS=("2022-$DD 0:00")
DATE_ENDS=("2022-$DD 23:59")


# Print array values in  lines
echo "Print every element in new line"
for hashtag in "${MACRON[@]}"; do
	echo -e $COLOR_CYAN "downloading..." "$hashtag" "${DATE_STARTS}" "${DATE_ENDS}" $COLOR_RESET
	poetry run python -m src data --task download --data twitter --text "$hashtag" --start_time "${DATE_STARTS}" --end_time "${DATE_ENDS}"
done

echo "Print every element in new line"
for hashtag in "${LEPEN[@]}"; do
	echo -e $COLOR_CYAN "downloading..." "$hashtag" "${DATE_STARTS}" "${DATE_ENDS}" $COLOR_RESET
	poetry run python -m src data --task download --data twitter --text "$hashtag" --start_time "${DATE_STARTS}" --end_time "${DATE_ENDS}"
done

# poetry run dvc add data
# poetry run dvc push
# git add data.dvc
# git commit -m $1
# git push
