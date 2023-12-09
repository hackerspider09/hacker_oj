#!/bin/bash

# n=7
# for (( i=1 ; i<=$n ; i++ )); 
# do
#     echo $i
# done

read -p "Enter the starting value: " start_value
read -p "Enter the ending value: " end_value

# Check if the inputs are valid positive integers

if [[ ! "$start_value" =~ ^[0-9]+$ || ! "$end_value" =~ ^[0-9]+$ || "$start_value" -lt 1 || "$end_value" -lt 1 || "$end_value" -lt "$start_value" ]]; then
  echo "Invalid input. Please enter valid positive integers with the ending value greater than or equal to the starting value."
  exit 1
fi

