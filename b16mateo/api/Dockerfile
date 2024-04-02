FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip \
    && pip install fastapi uvicorn psycopg2-binary requests

# port with which FastAPI is running
EXPOSE 8000

CMD ["python", "main.py"]



