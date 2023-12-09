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
    sudo rm -rf "$destination_folder"
  fi


  if [ "$(sudo docker ps -a | grep -c container$i)" -gt 0 ] ; then
    # If container exists delete it and create new
    echo "Container $i Exists"
    sudo docker stop "container$i" 

    echo "Remove Container $i"
    sudo docker rm "container$i"
  fi
done

echo "Judge Folder removed."
echo "Containers stopped and removed."
