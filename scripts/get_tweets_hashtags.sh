#! /bin/bash -

# Color related variables
COLOR_CYAN="\e[1;36m"
COLOR_PURPLE="\e[1;35m"
COLOR_RESET="\e[0m"

# request forging Twitter API related variables
LEPEN=("#Marine2022" "#MarinePresidenteDeTousLesFrancais" "#JeVoteMarine" \
	"#MarinePresidente" "#MarinePresidente2022" "#marine2022" "#MarinePrésidente" \
	"#MarineLePenPresidente" "#DimancheJeVoteMarine" "#Marine" "#Le24JeVoteMarine" '#Marinenoussauve'
   	'#JeVoteMarineLePen' '#LePen2022')
MACRON=("#Macron2022" "#JeVoteMacron" "#JeVoteMacronAuDeuxiemeTour" "#JeVoteMacron")
NEG=("#NiMacronNiLePenAbstention")
NEG_MACRON=("#ToutsaufMacron" "#ToutSaufMacron" "#Macronéron" "#SansLui" "#BarrageAMacron"\
	"#TousContreMacron" "#MacronDehors" "#Arrogant" "#mackinsey" "#TousSaufMacron"\
   	"#MacronMenteur" "#McKingseyGate" '#TousContreMacon' '#5ansdeplus','#ToutSaufMacon'\
   	'#McKinseyMacronGate' '#MacronDegage2022' '#MacronDegage' '#passvaccinal'\
	'#FranceBonToutouDesUs' '#ToutSaufMacon' '#MacronBenVoyons' '#McKinseyGate' '#MacronDegage'\
	'#macronnousprendpourdescons' '#MacroDehors' '#TousContreMacon' '#macarons2022')
NEG_LEPEN=("#NiMarineNiLePen" '#LePenNeDoitPasPasser' '#LePenNonMerci' )
HASHTAGS=("${LEPEN[@]}" "${MACRON[@]}" "${NEG[@]}" "${NEG_MACRON[@]}" "${NEG_LEPEN[@]}")
NEW=()
DD="04-25"
DATE_STARTS=("2022-$DD 0:00")
DATE_ENDS=("2022-$DD 23:59")


#Print array values in  lines
echo "Print every element in new line"
for hashtag in "${HASHTAGS[@]}"; do
	echo -e $COLOR_CYAN "downloading..." "$hashtag" "${DATE_STARTS}" "${DATE_ENDS}" $COLOR_RESET
	poetry run python -m src data --task download --data twitter --text "$hashtag" --start_time "${DATE_STARTS}" --end_time "${DATE_ENDS}"
done

echo "Print every element in new line"
for hashtag in "${NEW[@]}"; do
	echo -e $COLOR_CYAN "downloading..." "$hashtag" "${DATE_STARTS}" "${DATE_ENDS}" $COLOR_RESET
	poetry run python -m src data --task download --data twitter --text "$hashtag" --start_time "${DATE_STARTS}" --end_time "${DATE_ENDS}"
done

# poetry run dvc add data
# poetry run dvc push
# git add data.dvc
# git commit -m $1
# git push
