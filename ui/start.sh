#!/bin/sh

python manage.py makemigrations --noinput && \
python manage.py migrate --noinput && \
python manage.py runserver --insecure 0.0.0.0:8080