# Utilisez une image de Python officielle en tant qu'image de base
FROM python:3.10-slim

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez le contenu de votre projet FastAPI dans le répertoire de travail du conteneur
COPY . .

# # Installation des dépendances système nécessaires
# RUN apt-get update && apt-get install -y \
#     libgl1-mesa-glx \
#     libglib2.0-0 \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
RUN pip install --upgrade pip \
    && pip install fastapi uvicorn psycopg2-binary requests

# Exposez le port sur lequel votre application FastAPI fonctionne
EXPOSE 8000

# Commande pour démarrer votre application FastAPI
CMD ["python", "main.py"]



