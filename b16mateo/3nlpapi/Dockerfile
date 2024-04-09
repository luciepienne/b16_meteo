FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir fastapi uvicorn requests psycopg2-binary
    
# port with which FastAPI is running
EXPOSE 8002

# CMD ["uvicorn", "nlpapi:app", "--reload", "--host", "0.0.0.0", "--port", "8020"]
CMD ["python", "nlpapi.py"]


