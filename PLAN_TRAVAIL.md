# Plan de Travail - Améliorations Hotel Mediterranee

## 1. Information Gathered

### Fichiers analysés:
- **app.py** : Application principale Streamlit (~650 lignes)
- **config.yml** : Configuration Cloudflare Tunnel
- **start_internet.bat** : Script de lancement avec tunnel

### État actuel:
1. **URL**: Cloudflare Tunnel gratuit (URL temporaire change à chaque redémarrage)
2. **Connexion**: Session Streamlit (se perd à l'actualisation)
3. **Sons**: winsound (Windows only, ne fonctionne pas sur mobile/web)
4. **Notifications**: Toast Streamlit + son système Windows

---

## 2. Plan Détaillé

### Étape 1: URL Permanente (Cloudflare Tunnel Nommé)
- [ ] Créer un tunnel nommé "hotel-med" avec Cloudflare
- [ ] Configurer un sous-domaine permanent 
- [ ] Modifier config.yml pour utiliser le tunnel nommé
- [ ] Mettre à jour start_internet.bat

### Étape 2: Connexion Persistante
- [ ] Implémenter persistence via localStorage (JavaScript)
- [ ] Stocker les infos utilisateur dans le navigateur
- [ ] Restaurer la session au chargement de la page

### Étape 3: Sons de Notification Universels
- [ ] Ajouter fichiers audio dans le projet
- [ ] Implémenter lecture audio via JavaScript (fonctionne sur mobile/PC)
- [ ] Créer fonction play_notification_sound() universelle

### Étape 4: Améliorations UI/UX Mobile
- [ ] Optimiser les styles pour mobile
- [ ] Tester l'accessibilité depuis smartphone

---

## 3. Fichiers à Modifier

| Fichier | Modification |
|---------|--------------|
| app.py | Connexion persistante, sons universels |
| config.yml | Configuration tunnel nommé |
| start_internet.bat | Script avec URL fixe |

---

## 4. Suivi

- [ ] Étape 1: URL Permanente - En attente
- [ ] Étape 2: Connexion Persistante - En attente
- [ ] Étape 3: Sons Universels - En attente
- [ ] Étape 4: Tests Mobile - En attente

