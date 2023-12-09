echo "*************** Server Deactivating ***************"

sudo docker-compose down


echo "*************** Judge container stopping ***************"
bash "$(pwd)/stopContainer.sh"
