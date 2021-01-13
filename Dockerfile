FROM python:3.6.12-slim

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt ./manage.py /app/
COPY ./prospectiva /app/prospectiva
COPY ./georaffe /app/georaffe
WORKDIR /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
