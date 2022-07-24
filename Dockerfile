FROM python:3.7.13-slim-buster
WORKDIR /code
RUN apt-get update && apt-get install -y gcc libpq-dev
RUN /usr/local/bin/python -m pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/