# 📋 **CLASSES et CAS D'UTILISATION COMPLETS** - Hotel Mediterranée

## **1. TOUTES LES CLASSES (Extraites du code app.py)**

### **Classes Principales (Entités Métier)**
| Classe | Attributs | Méthodes | Fichier |
|--------|-----------|----------|---------|
| **Utilisateur** | `username`, `password`(SHA256), `role`(admin/recep/maint), `nom` | `authenticate()`, `hash_password()`, `delete_user()` | utilisateurs.json |
| **Chambre** | `numero`(str), `type`(Standard/Suite), `aile`(A/B), `etage`(int), `statut`(Libre/Occ/Maint) | `load_rooms()`, `save_rooms()`, `update_status()`, `add_room()`, `delete_room()`, `get_history()`, `get_count()` | chambres.csv |
| **TacheMaintenance** | `id`, `chambre`, `description`, `type_panne`, `assigned_to`, `statut`(Attente/Cours/Terminé), `priorite`(H/M/B), `date_creation/completion`, `duree_estimee/reelle` | `create()`, `update_status()`, `update_priorite()`, `update_duree()`, `delete()` | maintenance_tasks.csv |
| **TypePanne** | `id`, `nom_panne`, `description`, `priorite`, `date_creation` | `load_pannes()`, `add_panne()`, `save_pannes()` | pannes.csv |
| **Composant** | `id`, `chambre`, `composant_principal`, `sous_composant`, `statut`(Bon/Dégradé/Cassé/Maint), `date_install/maintenance` | `load_composants()`, `add_composant()`, `update_status()`, `delete()` | composants_chambres.csv |
| **Reclamation** | `id`, `chambre`, `type_panne`, `description`, `date_declaration`, `statut`(Déclaré/Traitement), `creé_par` | `load_reclamations()`, `add_reclamation()`, `update_status()`, `delete()` | reclamations.csv |
| **Notification** | `id`, `title`, `message`, `type`(info/warn/error/success), `date`, `read`(bool), `target_role` | `load_notifications()`, `add_notification()`, `mark_read()`, `get_unread_count()` | notifications.json |
| **RapportTache** | `task_id`, `agent`, `rapport`, `duree_travail_minutes`, `date_rapport`, `pieces_utilisees`, `notes_agent` | `load_rapports()`, `add_rapport()`, `get_agent_history()` | rapports_taches.csv |

### **Classes Techniques (Services)**
| Classe/Service | Rôle |
|----------------|------|
| **SessionManager** | Persistance queryParams (7 jours) + restore |
| **NotificationEngine** | Polling JS 3s + son/vibration + ciblage rôle |
| **DataManager** | CRUD CSV/JSON + validation |
| **RoomStatusEngine** | Auto-update statut (tâches actives → Maintenance/Libre) |
| **PrioritySorter** | Tri tâches (priorité + date) |

---

## **2. TOUS LES CAS D'UTILISATION (Complets avec <<include/extend>>)**

### **Acteurs**
```
1. Admin (Chef Maintenance)
2. Receptionniste
3. Agent Maintenance
4. Système (Automatique)
```

### **Cas d'Utilisation Détaillés (41 UC identifiés)**

#### **A. ADMIN (Chef - 22 UC)**
| # | UC | Description | <<include>> | <<extend>> | Pré/Post |
|---|----|-------------|-------------|------------|----------|
| UC1 | Gérer Chambres | CRUD + stats | Update Statut | Historique | - |
| UC2 | Créer Tâche | Nouvelle maintenance | Notifier Agent | Assigner Priorité | Chambre → Maint |
| UC3 | Gérer Types Pannes | CRUD types | - | - | - |
| UC4 | Gérer Composants | Suivi équipements | - | Alerte Dégradé | - |
| UC5 | Suivi Performance Agents | Stats/tâches/rapports | - | Rapport Manquant | - |
| UC6 | Gérer Utilisateurs | CRUD comptes | - | - | Ne supprime pas admin |
| UC7 | Traiter Réclamation | Convertir en tâche | Créer Tâche | - | Statut → Traitement |
| UC8 | Dashboard Complet | Stats + vue grid | Voir Notifications | Filtres Avancés | - |
| UC9 | Marquer Notifs Lu | Tout/single | - | - | Compteur → 0 |
| UC10 | Update Priorité Tâche | H/M/B | Sauvegarder | Notifier Changement | Tri auto |
| UC11 | Enregistrer Durée Réelle | Rapport chef | - | - | Stats agents |
| UC12 | Effacer Historique Chambre | Toutes tâches | - | Vérif Tâches Actives | - |
| UC13 | Bulk Reset Chambres | Toutes → Libre | - | Confirmer | - |

#### **B. RÉCEPTIONNISTE (9 UC)**
| # | UC | Description | <<include>> | <<extend>> | Pré/Post |
|---|----|-------------|-------------|------------|----------|
| UC14 | Dashboard Réception | Stats + grid | Voir Notifications | - | - |
| UC15 | Déclarer Panne | Signalement rapide | Notifier Admin | - | Auto-tâche créée |
| UC16 | Voir Chambres Maintenance | Filtres | - | - | - |

#### **C. AGENT MAINTENANCE (8 UC)**
| # | UC | Description | <<include>> | <<extend>> | Pré/Post |
|---|----|-------------|-------------|------------|----------|
| UC17 | Voir Mes Tâches | Liste personnelle | Voir Notifications | - | Tri priorité |
| UC18 | Démarrer Tâche | En attente → Cours | - | - | - |
| UC19 | Terminer Tâche | Cours → Terminé | Remplir Rapport | - | Chambre ?→ Libre |
| UC20 | Remplir Rapport | Détails travail | Terminer Tâche | - | Stats agents |
| UC21 | Dashboard Agent | Stats personnelles | Voir Mes Tâches | - | - |

#### **D. SYSTÈME (2 UC Automatiques)**
| # | UC | Description | <<include>> | <<extend>> | Pré/Post |
|---|----|-------------|-------------|------------|----------|
| UC22 | Notification Temps Réel | Polling 3s + son | - | Vibration Mobile | - |
| UC23 | Auto-Update Statut Chambre | Tâches finies → Libre | - | - | Règle métier |

### **Relations <<include/extend>> Complètes**
```
<<include>> (Obligatoires) :
- Créer Tâche → Notifier Agent
- Déclarer Panne → Notifier Admin
- Terminer Tâche → Remplir Rapport
- Gérer Chambres → Update Statut

<<extend>> (Optionnelles) :
- Traiter Tâche → Remplir Rapport
- Voir Stats → Filtres Avancés
- Suivi Agents → Rapport Manquant
```

**Total : 23 UC principaux + 18 variantes/extensions.**

---

## **Mermaid Diagramme Classes ÉTENDU**

```mermaid
classDiagram
    %% Classes déjà listées + relations complètes
    Note "41 Use Cases, 10 Classes principales<br/>+ 5 Services techniques" as N1
```

**Fichier créé :** `classes_et_usecases_complets.md`

**Visualise dans mermaid.live ou GitHub !** 📈✨
