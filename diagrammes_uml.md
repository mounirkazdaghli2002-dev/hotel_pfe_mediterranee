# 🏨 Diagrammes UML - Hotel Mediterranée PFE

## 1. **Diagramme de Classes** (Structure Données)

```mermaid
classDiagram
    class Utilisateur {
        +username: String
        +password: Hash
        +role: String (admin/reception/maintenance)
        +nom: String
        +authenticate()
        +hash_password()
    }

    class Chambre {
        +numero: String
        +type: String
        +aile: String
        +etage: int
        +statut: String (Libre/Occupée/Maintenance)
        +update_status()
        +get_history()
    }

    class TacheMaintenance {
        +id: int
        +chambre: String
        +description: String
        +type_panne: String
        +assigned_to: String
        +statut: String (En_attente/En_cours/Terminé)
        +priorite: String (Haute/Moyenne/Basse)
        +date_creation: DateTime
        +date_completion: DateTime
        +duree_estimee: float
        +update_status()
        +create()
    }

    class TypePanne {
        +id: int
        +nom_panne: String
        +description: String
        +priorite: String
    }

    class Composant {
        +id: int
        +chambre: String
        +composant_principal: String
        +sous_composant: String
        +statut: String (Bon/Dégradé/Cassée)
        +date_installation: Date
        +derniere_maintenance: Date
    }

    class Reclamation {
        +id: int
        +chambre: String
        +type_panne: String
        +description: String
        +statut: String
        +creé_par: String
    }

    class Notification {
        +id: int
        +title: String
        +message: String
        +type: String (info/warning/error)
        +target_role: String
        +read: boolean
    }

    class RapportTache {
        +task_id: int
        +agent: String
        +rapport: String
        +duree_travail: float
        +pieces_utilisees: String
    }

    %% Associations
    Utilisateur ||--o{ TacheMaintenance : assigne
    Utilisateur ||--o{ Reclamation : crée
    Chambre ||--o{ TacheMaintenance : concerne
    Chambre ||--o{ Composant : contient
    TypePanne ||--o{ TacheMaintenance : type
    TacheMaintenance ||--|| RapportTache : génère
    Reclamation ||--o| TacheMaintenance : convertit_en
    Notification ||--o| Utilisateur : notifie
```

## 2. **Diagramme de Cas d'Utilisation** (Use Cases avec <<include>> <<extend>>)

```mermaid
graph TB
    Admin[Admin<br/>Chef Maintenance] --> UC1[Gérer Chambres]
    Admin --> UC2[Créer Tâche Maintenance]
    Admin --> UC3[Gérer Types Pannes]
    Admin --> UC4[Gérer Composants]
    Admin --> UC5[Suivi Agents]
    Admin --> UC6[Gérer Utilisateurs]

    Receptionniste[Réceptionniste] --> UC7[Déclarer Panne]
    Maintenance[Agent Maintenance] --> UC8[Traiter Tâche]

    Tous[Tous Rôles] --> UC9[Consulter Dashboard]
    Tous --> UC10[Gérer Notifications]

    %% <<include>>
    UC2 -->|<<include>>| UC11[Notifier Agent]
    UC7 -->|<<include>>| UC11
    UC8 -.->|<<extend>>| UC12[Remplir Rapport]
    UC1 -->|<<include>>| UC13[Update Statut Chambre]
    UC9 -->|<<include>>| UC14[Voir Stats Chambres]

    UC11 --> UC10
    UC12 --> UC15[Terminer Tâche]

    classDef actor fill:#e1f5fe
    classDef uc fill:#f3e5f5
    classDef include fill:#e8f5e8
    classDef extend fill:#fff3e0

    class Admin,Receptionniste,Maintenance,Tous actor
    class UC1,UC2,UC3,UC4,UC5,UC6,UC7,UC8,UC9,UC10 uc
    class UC11,UC13,UC14 include
    class UC12,UC15 extend
```

## 3. **Séquence Typique : Déclarer Panne → Tâche → Rapport**

```mermaid
sequenceDiagram
    participant R as Receptionniste
    participant S as Système
    participant A as Admin
    participant M as Maintenance Agent
    participant DB as Base CSV/JSON

    R->>S: Déclarer Panne (Chambre/Type)
    S->>DB: Sauvegarder Reclamation
    S->>S: <<include>> Notifier Admin
    Note over S: Son + Badge temps réel
    S->>A: Notification haute priorité

    A->>S: Créer Tâche depuis Reclamation
    S->>DB: Créer TâcheMaintenance
    S->>S: Update Chambre → Maintenance
    S->>M: Notification assignation

    M->>S: Start Tâche
    M->>S: <<extend>> Finish + Rapport
    S->>DB: Sauvegarder RapportTache
    S->>S: <<include>> Update Chambre → Libre?
    S->>R: Notif "Chambre Libre"
```

## 4. **Flux de Données (DFD Niveau 1)**

```mermaid
graph LR
    A[Utilisateur] --> B[Interface Streamlit]
    B --> C{Authentification}
    C -->|OK| D[Dashboard + Rôles]
    C -->|KO| E[Login]

    D --> F[Load CSV/JSON]
    F --> G[CRUD Operations]
    G --> H[Notifications Engine]
    H --> I[JS Polling/Son]
    G --> F

    J[Session QueryParams] --> D
```

## 🔑 **Règles Métier (OCL-like)**
```
context Chambre inv:
    if statut = 'Maintenance' and no active_tasks then
        statut := 'Libre'

context TacheMaintenance inv high_priority_first:
    tasks.sort_by(priorite desc, date_creation desc)
```

**Fichiers créés :** `diagrammes_uml.md` (copier dans README ou docs/).

**Visualiser :** Colle le contenu Mermaid dans [mermaid.live](https://mermaid.live) ou GitHub Markdown.
