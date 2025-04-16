FROM python:3.12.8-slim
LABEL maintainer="oleksandr.tsvirko@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR app/

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config

RUN pip install -r requirements.txt

COPY . .

RUN adduser \
        --disabled-password \
        --no-create-home \
        my_user

USER my_user