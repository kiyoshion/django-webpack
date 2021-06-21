#!/bin/sh

python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
npm install
npm run dev

exec "$@"
