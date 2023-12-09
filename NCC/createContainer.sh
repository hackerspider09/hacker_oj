#!/bin/bash

# Run file with bash not sh 

# Prompt the user for the starting and ending values
read -p "Enter the starting value: " start_value
read -p "Enter the ending value: " end_value


# Check if the inputs are valid positive integers
if [[ "$start_value" -lt 1 || "$end_value" -lt 1 || "$end_value" -lt "$start_value" || "$end_value" -gt 30 || "$start_value" -gt 30 ]]; then
  echo "Invalid input. Please enter valid positive integers with the ending value greater than or equal to the starting value."
  exit 1
fi


# Define the source folder
# source_folder="/path/to/source_folder"
source_folder="$(pwd)/Judge/mainFolder"

# # Check if the source folder exists
if [ ! -d "$source_folder" ]; then
  echo "Source folder does not exist."
  exit 1
fi

# Loop to create copies of the folder and run Docker containers
for ((i = start_value; i <= end_value; i++)); do
  destination_folder="$(pwd)/Judge/container$i/"

  # Check if the destination folder already exists and delete it
  if [ -d "$destination_folder" ]; then
    rm -rf "$destination_folder"
  fi

  # Create a new destination folder
  mkdir -p "$destination_folder"


  # Copy the source folder to the destination
  cp -r $source_folder/* $destination_folder

  # Check if the copy was successful
  if [ $? -eq 0 ]; then
    echo "Copied to $destination_folder"
  else
    echo "Failed to copy to $destination_folder"
    continue  # Skip creating the Docker container if the copy failed
  fi


# method 2 create docker container
  if [ "$(sudo docker ps -a | grep -c container$i)" -gt 0 ] ; then
    # If container exists delete it and create new
    echo "Container $i Exists"
    sudo docker stop "container$i" 

    echo "Remove Container $i"
    sudo docker rm "container$i"
  fi
  echo "Container $i created"

  # It will create new container
  sudo docker run -d -it --memory="200m" --name "container$i" -v "$destination_folder:/src" --security-opt seccomp="$(pwd)/seccomp/script.json" python bash

done

echo "Copied and created containers from $start_value to $end_value."
