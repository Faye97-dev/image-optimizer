# Dockerfile

# pull the official docker image
FROM python:3.8.10-slim

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy project
COPY . .

RUN chmod -R 777 /app/logs
RUN chmod -R 777 /app/storage


