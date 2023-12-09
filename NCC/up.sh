echo "*************** Server starting ***************"

echo "*************** Judge container creating ***************"
bash "$(pwd)/container.sh"

sleep 2

echo "*************** Running compose Up ***************"
sudo docker-compose up --build --scale web=3

