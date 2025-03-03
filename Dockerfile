# Utiliser une image Python de base (3.9-slim-buster)
FROM python:3.9-slim-buster

# Définir le dossier de travail
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le reste du code source
COPY . .

# Définir le HEALTHCHECK en utilisant l'endpoint /health
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8000/health || exit 1

# Exécuter votre script Python
CMD ["python", "main.py"]
