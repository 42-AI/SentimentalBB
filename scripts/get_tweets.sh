#! /bin/bash -

# Color related variables
COLOR_CYAN="\e[1;36m"
COLOR_PURPLE="\e[1;35m"
COLOR_RESET="\e[0m"

# request forging Twitter API related variables
CANDIDATS=("Pecresse" "Zemmour" "Dupont-Aignan" "Melenchon" "Le Pen" "Lassalle" "Hidalgo" "Macron" "Jadot" "Roussel" "Arthaud" "Poutou")
DD="04-06"
DATE_STARTS=("2022-$DD 0:00" "2022-$DD 4:00" "2022-$DD 8:00" "2022-$DD 12:00" "2022-$DD 16:00" "2022-$DD 20:00")
DATE_ENDS=("2022-$DD 4:00" "2022-$DD 8:00" "2022-$DD 12:00" "2022-$DD 16:00" "2022-$DD 20:00" "2022-$DD 23:59")


# Print array values in  lines
echo "Print every element in new line"
for candidat in "${CANDIDATS[@]}"; do
    for i in "${!DATE_STARTS[@]}"; do
        echo -e $COLOR_CYAN "downloading..." "$candidat" "${DATE_STARTS[i]}" "${DATE_ENDS[i]}" $COLOR_RESET
        poetry run python -m src data --task download --data twitter --candidate "$candidat" --start_time "${DATE_STARTS[i]}" --end_time "${DATE_ENDS[i]}"
    done
    echo -e $COLOR_PURPLE "... sleeping 30 seconds to avoid limit rate ..." $COLOR_RESET
    sleep 30
done

# poetry run dvc add data
# poetry run dvc push
# git add data.dvc
# git commit -m $1
# git push
