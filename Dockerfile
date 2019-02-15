FROM ubuntu:latest
FROM python:3.7

RUN apt-get update
RUN apt-get install -y ffmpeg

RUN python -m pip install pipenv

COPY . /var/movie-meme-generator/
WORKDIR /var/movie-meme-generator

RUN pipenv install

ENTRYPOINT [ "pipenv", "run", "python", "movie-meme-generator.py" ]