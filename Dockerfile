# Utiliser une image Python de base (3.9-slim-buster)
FROM python:3.9-slim-buster

# Installer curl pour la commande HEALTHCHECK
RUN apt-get update && apt-get install -y curl

# Définir le dossier de travail
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Installer gunicorn
RUN pip install gunicorn

# Copier tout le reste du code source
COPY . .

# Définir le HEALTHCHECK en utilisant l'endpoint /health
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8000/health || exit 1

# Exposer le port sur lequel l'application s'exécute
EXPOSE 8000

# Exécuter l'application avec Gunicorn
# Remplacez "app:app" par votre module et variable d'application
# Par exemple, si votre application est dans main.py et l'instance s'appelle 'app'
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "main:app"]
