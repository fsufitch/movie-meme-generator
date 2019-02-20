#!/bin/sh

docker build -f Dockerfile.script -t moviememes:script . || exit 1
docker run --name moviememes-script \
    -v $(readlink -f ./resources):/app/resources \
    moviememes:script || exit 1
docker cp moviememes-script:/app/output.jpg output.jpg
docker rm moviememes-script
