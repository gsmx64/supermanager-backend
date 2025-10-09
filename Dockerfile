FROM python:3.14.0-slim AS build-phase

WORKDIR /app-build

ENV PRODUCTION=true
ENV ENVIRONMENT=production
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY requirements.txt ./

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app-build/wheels -r requirements.txt


FROM python:3.14.0-slim

RUN mkdir -p /home/app && addgroup --system app && adduser --system --group app && mkdir /home/app/web

WORKDIR /home/app/web

ENV PRODUCTION=true
ENV ENVIRONMENT=production
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends netcat
COPY --from=build-phase /app-build/wheels /wheels
COPY --from=build-phase /app-build/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache /wheels/*

COPY . /home/app/web

RUN chown -R app:app /home/app/web

USER app

EXPOSE 8000

CMD ["uvicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--worker-class", "uvicorn.workers.UvicornWorker", "supermanager.asgi:api"]
