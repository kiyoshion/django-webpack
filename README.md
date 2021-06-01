# Django DRUD app on Docker

Django + Nginx + Gunicorn

## Setup environment

1. Make Pipfile
2. Install pipenv and packages

```bash[bash]
cd app
pip install pipenv
pipenv install
pipenv shell
(app) django-admin.py startproject config .
(app) python manage.py migrate
(app) python manage.py runserver
```

## Setup docker

1. Make Dockerfile for Django
2. Make dokcer-compose.yml for Django

## Update settings.py

1. SECRET_KEY
2. DEBUG
3. ALLOWED_HOSTS

## Start via docker-compose

```bash[bash]
docker-compose up -d --build
```

## Setup postgres

1. Add postgres service in docker-compose.yml
2. Update .env for postgresql
3. Update settings.py
4. Update Dockerfile for psycopg2

Up docker-compose and migrate. So we can see welcome page on localhost:8000.

```bash[bash]
docker-compose down -v
docker-compose up -d --build
docker-compose exec django python manage.py migrate
```
