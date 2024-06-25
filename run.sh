source .env

git pull

sudo docker compose config > docker-compose.processed.yml

sed -i '/published:/ s/"//g' docker-compose.processed.yml
sed -i '/^name: .*/d' docker-compose.processed.yml

sudo docker stack deploy -c ./docker-compose.processed.yml "$STACK_NAME"