# TODO - Hotel Mediterranee - Système de Gestion

## Fonctionnalités Implémentées

### Phase 1 : Authentification et Rôles ✅
- [x] Page de connexion
- [x] Trois rôles: Admin, Réceptionniste, Agent Maintenance
- [x] Gestion des utilisateurs (CRUD)

### Phase 2 : Gestion des Chambres ✅
- [x] Affichage des chambres avec statut (Libre, Occupée, Maintenance)
- [x] Filtres par aile, étage, statut
- [x] Modification automatique du statut selon clients/check-in

### Phase 3 : Gestion des Clients ✅
- [x] Enregistrement check-in
- [x] Check-out automatique
- [x] Liaison chambre-client automatique

### Phase 4 : Maintenance ✅
- [x] Création de tâches de maintenance
- [x] Assignment aux agents
- [x] Suivi du statut (En attente → En cours → Terminé)
- [x] Notification admin lors de la fin de tâche

### Phase 5 : Notifications ✅
- [x] Notifications pour l'admin
- [x] Marquer comme lu

---

## Comptes par défaut

| Rôle | Username | Mot de passe |
|------|----------|--------------|
| Admin | admin | admin123 |
| Réceptionniste | receptionniste | reception123 |
| Maintenance | maintenance | maintenance123 |

---

## Statut des Chambres (Logique Automatique)

- **Occupée**: Quand un client actif est assigné à la chambre
- **Libre**: Quand aucun client actif ET aucune tâche active
- **Maintenance**: Quand une tâche de maintenance est en cours

---

## Comment lancer l'application

```bash
python -m streamlit run app.py --server.port=8501
```

Puis ouvrez: **http://localhost:8501**

---

## Progression
10/10 tâches complétées ✅

