#git stash
git pull
docker build --tag pilstoken-bot .
chmod +x update.sh
docker-compose down
docker-compose up -d
