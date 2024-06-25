sudo docker compose config > docker-compose.processed.yml

sed -i '/published:/ s/"//g' docker-compose.processed.yml
sed -i '/^name: .*/d' docker-compose.processed.yml