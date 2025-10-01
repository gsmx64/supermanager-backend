#!/bin/bash
echo -----------------------------------------
echo > Running App Backend - Development
echo -----------------------------------------
export ENVIRONMENT=development
source .env.development && ./env/bin/python manage.py runserver && cd.. && exit 0