#!/bin/bash

echo "Running Database migrations..."
python manage.py migrate

echo "Creating superuser..."
python manage.py createsuperuser --noinput

echo "Loading initial data..."
python manage.py loaddata fixtures/oauth2_provider.application.json --app oauth2_provider.application

echo "Running the Server..."
python manage.py runserver 0.0.0.0:8000