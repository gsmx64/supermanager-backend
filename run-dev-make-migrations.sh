#!/bin/bash
echo -----------------------------------------
echo > Running App Backend - Development
echo -----------------------------------------
export ENVIRONMENT=development
source .env.development && ./env/bin/python manage.py makemigrations && ./env/bin/python manage.py migrate && exit 0