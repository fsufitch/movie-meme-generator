#!/bin/sh

docker build -t moviememes . || exit 1
docker run --name moviememes moviememes || exit 1
docker cp moviememes:/var/movie-meme-generator/output.jpg output.jpg
docker rm moviememes