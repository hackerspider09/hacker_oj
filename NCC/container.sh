#!/bin/bash


# At start when server is started this bash file will automaticaly create 12 container
# For emergency user createContainer.sh 


# source_folder="/path/to/source_folder"
source_folder="$(pwd)/Judge/mainFolder"


# Loop to create copies of the folder and run Docker containers
# MH12

for ((i = 1; i <= 12; i++)); do
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

echo "Copied and created containers 1 to 12"
