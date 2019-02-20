#!/bin/sh

docker build -f Dockerfile.server -t moviememes . || exit 1
docker run --rm --name moviememes -p 8080:8080 moviememes || exit 1
