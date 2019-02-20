#!/bin/sh

docker build -f Dockerfile.script -t moviememes . || exit 1
docker run --name moviememes moviememes || exit 1
docker cp moviememes:/app/output.jpg output.jpg
docker rm moviememes
