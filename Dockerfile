# Utiliser une image Python de base
FROM python:3.9-slim-buster

# Définir des variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Créer un utilisateur non-root
RUN adduser --disabled-password --gecos "" appuser

# Définir le dossier de travail
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn

# Copier tout le reste du code source
COPY . .

# Changer le propriétaire des fichiers de l'application
RUN chown -R appuser:appuser /app

# Passer à l'utilisateur non-root
USER appuser

# Exposer le port sur lequel l'application écoute
EXPOSE $PORT

# Ajouter un healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/ || exit 1

# Exécuter l'application avec Gunicorn
CMD gunicorn --bind 0.0.0.0:$PORT main:app
