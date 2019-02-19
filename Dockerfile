FROM ubuntu:latest
FROM python:3.7

RUN apt-get update
RUN apt-get install -y ffmpeg

RUN python -m pip install pipenv

WORKDIR /var/movie-meme-generator
COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install

COPY . .

ENTRYPOINT [ "pipenv", "run", "python", "movie-meme-generator.py", "movie-meme-config.yaml", "-m", "script"]