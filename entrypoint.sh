#!/bin/sh

# django
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --no-input

# gunicorn 
gunicorn -w 4 config.wsgi --bind 0.0.0.0:8000 
