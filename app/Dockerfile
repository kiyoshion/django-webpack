FROM python:3.7-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip \
&& pip install pipenv

COPY ./Pipfile /usr/src/app/Pipfile

RUN pipenv install --skip-lock --system --dev

COPY . /usr/src/app/
