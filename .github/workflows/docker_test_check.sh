#!/usr/bin/env bash

# Checks that the docker test run succeeded

# Define expected results
EXPECTED_FILES=("rgb_plot.csv")
EXPECTED_GREENNESS_VALUES=(2.3 0 20.55 1.6 52.72 -50.42 22.85 10.66 1.01 0.0 0.33)

# What folder are we looking in for outputs
if [[ ! "${1}" == "" ]]; then
  TARGET_FOLDER="${1}"
else
  TARGET_FOLDER="./outputs"
fi

# What our target file to read is
if [[ ! "${2}" == "" ]]; then
  CHECK_FILE="${2}"
else
  CHECK_FILE="rgb_plot.csv"
fi
EXPECTED_FILES+=("${CHECK_FILE}")

# Check if expected files are found
for i in $(seq 0 $(( ${#EXPECTED_FILES[@]} - 1 )))
do
  if [[ ! -f "${TARGET_FOLDER}/${EXPECTED_FILES[$i]}" ]]; then
    echo "Expected file ${EXPECTED_FILES[$i]} is missing"
    exit 10
  fi
done

# Check the results of the canopy cover calculation
RESULT_VALUES=(`gawk '
BEGIN {
    FPAT = "([^,]+)|(\"[^\"]+\")"
}
{
  if ($1 != "species") { # Skipping the header line
    printf("(%s %s %s %s %s %s %s %s %s %s %s)\n", $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17)
  }
}
END {
}
' "${TARGET_FOLDER}/${CHECK_FILE}"`)

echo "Result counts: ${#EXPECTED_GREENNESS_VALUES[@]} vs ${#RESULT_VALUES[@]}"
if [[ ${#EXPECTED_GREENNESS_VALUES[@]} != ${#RESULT_VALUES[@]} ]]; then
  echo "Number of results found in file (${#RESULT_VALUES[@]}) don't match expected count (${#EXPECTED_GREENNESS_VALUES[@]})"
  if [[ ${#RESULT_VALUES[@]} > 0 ]]; then
    for i in $(seq 0 $(( ${#RESULT_VALUES[@]} - 1 )))
    do
      echo "${i}: ${RESULT_VALUES[$i]}"
    done
  fi
  exit 20
fi

#for i in $(seq 0 $(( ${#EXPECTED_GREENNESS_VALUES[@]} - 1 )))
#do
#  # Check that we have the same number values
#  CUR_EXPECTED=${EXPECTED_GREENNESS_VALUES[$i]}
#  CUR_VALUES=${RESULT_VALUES[$i]}
#  if [[ ${#CUR_EXPECTED[@]} != ${#CUR_VALUES[@]} ]]; then
#    echo "Row ${i}: Expected ${#CUR_EXPECTED[@]} values and received ${#CUR_VALUES[@]}"
#    exit 30
#  fi
#
#  # Check each of the values
#  for j in $(seq 0 $(( ${#CUR_EXPECTED[@]} - 1 )))
#  do
#    if [[ "${CUR_EXPECTED[$j]}" == "${CUR_VALUES[$j]}" ]]; then
#      echo "Values for index ${j} match: '${CUR_EXPECTED[$j]}' '${CUR_VALUES[$j]}'"
#    else
#      echo "Result value for index ${j}: '${CUR_EXPECTED[$j]}' doesn't match expected: '${CUR_VALUES[$j]}'"
#      exit 30
#    fi
#  done
#done
