FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip && pip3 install -r requirements.txt --no-cache-dir

COPY ./ .
