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
