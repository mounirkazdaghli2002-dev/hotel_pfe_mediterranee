# 🐳 Guide Docker - Hotel Mediterranee

## 📋 Prérequis

- Docker Desktop installé (https://www.docker.com/products/docker-desktop)
- Docker Compose (inclus dans Docker Desktop)

## 🚀 Démarrage rapide

### Option 1: Avec Docker Compose (Recommandé)

```bash
# Construire et démarrer l'app
docker-compose up -d

# L'app sera accessible à http://localhost:8501
```

### Option 2: Build et Run manuel

```bash
# Construire l'image
docker build -t hotel-app:latest .

# Démarrer le conteneur
docker run -d \
  --name hotel-mediterranee \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/hotel_mediterranee.db:/app/hotel_mediterranee.db \
  hotel-app:latest
```

## 📍 Accès à l'application

- **URL locale**: http://localhost:8501
- **URL depuis autre machine**: http://<IP_DE_VOTRE_PC>:8501

## 🛑 Arrêter l'application

```bash
# Avec Docker Compose
docker-compose down

# Ou manuellement
docker stop hotel-mediterranee
docker rm hotel-mediterranee
```

## 📊 Commandes utiles

```bash
# Voir les logs en temps réel
docker-compose logs -f

# Voir les logs d'un conteneur spécifique
docker logs -f hotel-mediterranee

# Vérifier l'état des conteneurs
docker-compose ps

# Nettoyer les images non utilisées
docker image prune

# Reconstruire l'image (après modification du code)
docker-compose up -d --build
```

## 🔧 Environnement et Configuration

### Variables d'environnement

Créez un fichier `.env` à la racine du projet:

```env
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
```

### Volumes

- `/app/data`: Dossier pour les données persistantes
- `/app/hotel_mediterranee.db`: Base de données SQLite
- `/app/.streamlit`: Configuration Streamlit

## 📦 Push vers un registry (Docker Hub, ECR, etc.)

```bash
# Taguer l'image
docker tag hotel-app:latest <votre_username>/hotel-app:latest

# Push vers Docker Hub
docker push <votre_username>/hotel-app:latest

# Ou pour un registry personnalisé
docker tag hotel-app:latest <registry_url>/hotel-app:latest
docker push <registry_url>/hotel-app:latest
```

## 🆘 Dépannage

### Le conteneur s'arrête immédiatement
```bash
# Vérifier les logs
docker logs hotel-mediterranee
```

### Port 8501 déjà utilisé
```bash
# Modifier le port dans docker-compose.yml
# Changer "8501:8501" en "8502:8501"
docker-compose down
docker-compose up -d
```

### Problèmes de permissions
```bash
# Sur Linux/Mac
sudo chown -R $USER:$USER ./data
chmod -R 755 ./data
```

## 💾 Sauvegarde et Restauration

```bash
# Sauvegarder les données
docker cp hotel-mediterranee:/app/hotel_mediterranee.db ./backup/

# Restaurer les données
docker cp ./backup/hotel_mediterranee.db hotel-mediterranee:/app/
```

## 🔒 Production

Pour la production, considérez:

1. Utiliser un orchestrateur (Kubernetes, Docker Swarm)
2. Ajouter un reverse proxy (Nginx, Traefik)
3. Configurer HTTPS/SSL
4. Ajouter des limites de ressources
5. Mettre en place une stratégie de backup

Exemple limites Docker Compose:
```yaml
services:
  hotel-app:
    ...
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```
