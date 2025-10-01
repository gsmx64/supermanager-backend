@ECHO OFF
ECHO "-----------------------------------------"
ECHO "> Running App Backend - Development"
ECHO "-----------------------------------------"
SET ENVIRONMENT=development
env\Scripts\python.exe manage.py runserver
IF ERRORLEVEL 1 GOTO finish

:finish
PAUSE