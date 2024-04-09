# Utiliser une image Python officielle comme base
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install psycopg2-binary meteofrance_api

CMD ["python", "batch.py"]


