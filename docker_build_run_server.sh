#!/bin/sh

PORT=${PORT:-8080}

docker build -f Dockerfile.server -t moviememes:server . || exit 1
docker run -d --name moviememes-server -p $PORT:8080 --restart unless-stopped \
    -v $(readlink -f ./resources):/app/resources \
    moviememes:server || exit 1
