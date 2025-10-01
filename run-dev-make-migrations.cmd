@ECHO OFF
ECHO "-----------------------------------------"
ECHO "> Running App Backend - Development"
ECHO "> Making Migrations"
ECHO "-----------------------------------------"
SET ENVIRONMENT=development
env\Scripts\python.exe manage.py makemigrations
PAUSE
env\Scripts\python.exe manage.py migrate
IF ERRORLEVEL 1 GOTO finish

:finish
PAUSE