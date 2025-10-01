@ECHO OFF
ECHO "-----------------------------------------"
ECHO "> Runing App Frontend - Production Docker Build"
ECHO "-----------------------------------------"
SET NODE_ENV=production
SET APP_BUILD_NUMBER=1.0.0
IF NOT EXIST .env.production COPY /-Y .env.production.sample .env.production
docker build -t supermanager-frontend:%APP_BUILD_NUMBER% -f Dockerfile.prod .
IF ERRORLEVEL 1 GOTO finish

:finish
PAUSE