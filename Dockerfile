FROM python:3.8.5

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN mkdir -p /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .