# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN ls -l
COPY ./requirements.txt /code/
RUN pip install -r requirements.txt
COPY . .


