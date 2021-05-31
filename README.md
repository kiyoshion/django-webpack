# Django DRUD app on Docker

Django + Nginx + Gunicorn

## Setup environment

1. Make Pipfile
2. Install pipenv and packages

```bash[bash]
pip install pipenv
pipenv install
pipenv shell
(django-crud) django-admin startproject config .
(django-crud) python manage.py migrate
(django-crud) python manage.py runserver
```
