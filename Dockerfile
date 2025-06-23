FROM python:3.13-alpine

WORKDIR /app

COPY . /app

RUN apk add --no-cache \
    build-base \
    openssl-dev \
    python3-dev \
    musl-dev 

RUN pip install --no-cache-dir \
    -r ./gui/requirements.txt
