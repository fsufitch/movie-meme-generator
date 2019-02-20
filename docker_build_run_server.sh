#!/bin/sh

PORT=${PORT:-8080}

docker build -f Dockerfile.server -t moviememes:server . || exit 1
docker run --rm --name moviememes-server -p $PORT:8080 \
    -v $(readlink -f ./resources):/app/resources \
    moviememes:server || exit 1
