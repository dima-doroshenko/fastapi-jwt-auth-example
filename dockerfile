FROM python:3.12.1-slim

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .