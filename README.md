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

### Setup auto migrate

1. Add entrypoint.sh
2. chmod +x entrypoint.sh
3. Update Dockerfile

```bash[bash]
chmod +x app/entrypoint.sh
```


## Setup Gunicorn

1. Add gunicorn in Pipfile
2. Add docker-compose.prod.yml and update
3. Add entrypoint.prod.sh
4. Add Dockerfile.prod
5. Update docker-compose.prod.yml for new Dockerfile.prod
6. CMD and check localhost:8000/admin

```bash[bash]
docker-compose down -v
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec django python manage.py migrate --noinput
```


## Setup Nginx

1. Make nginx dir to root
2. Add Dockerfile
3. Add nginx.conf
4. Add nginx in docker-compose.prod.yml
5. Check connection of nginx

```bash[bash]
docker-compose down -v
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec django python manage.py migrate --noinput
```


## Setup static file

1. Update settings.py
2. Update entrypoint.sh for collectstatic command
3. Update docker-compose.prod.yml for staticfiles
4. Update nginx.conf for staticfiles

```bash[bash]
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec django python manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec django python manage.py collectstatic
```
