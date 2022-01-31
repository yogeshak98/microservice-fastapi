FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /app/