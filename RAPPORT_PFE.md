# Rapport de Projet de Fin d'Études

## République Tunisienne
Ministère de l'Enseignement Supérieur et de la Recherche Scientifique  
Ecole Supérieure Privée des Technologies de l'Information et de Management de Nabeul

---

## Rapport de Projet de Fin d'Etudes
soumis afin d'obtenir le  
**Diplôme National d'Ingénieur en Business Intelligence**

### Réalisé par
**[Votre Nom]**

**Plateforme Web de Gestion Hôtelière**  
Système Intelligent de Réservation et Maintenance

### Encadrant Académique
Madame/Monsieur [Nom Encadrant]

### Encadrant Professionnel
M [Nom Professionnel]

### Projet de Fin d'Etudes fait à
**Hôtel Méditerranée Nabeul**

### Année Universitaire 2024-2025

---

## Dédicaces

Je tiens à exprimer ma sincère gratitude à mon encadrant académique, pour ses conseils avisés, 
sa bienveillance et son soutien constant tout au long de ce projet. Son expertise et sa disponibilité 
m'ont été d'une grande aide, et je lui suis profondément reconnaissant pour son accompagnement.

Je dédie également ce travail à mon encadrant professionnel, dont les remarques pertinentes et 
l'expertise métier ont grandement contribué à l'amélioration de cette solution. Sa vision du secteur 
hôtelier m'a permis de développer une application vraiment adaptée aux besoins du terrain.

Enfin, je ne saurais oublier ma famille et mes proches, qui m'ont apporté un soutien inestimable, 
non seulement durant la période de ce projet, mais tout au long de ma vie. Leur amour, leur 
encouragement et leur présence ont été une source de motivation constante.

---

## Remerciement

La réalisation de ce projet de fin d'études a été une expérience enrichissante et formatrice. 
Je tiens à exprimer ma profonde gratitude envers toutes les personnes qui ont contribué, de près 
ou de loin, à son aboutissement.

Je remercie l'École Supérieure Privée des Technologies d'Information et de Management de Nabeul 
pour la qualité de l'enseignement dispensé et le soutien apporté tout au long de mon parcours 
académique.

J'exprime également ma gratitude envers l'établissement hôtelier qui m'a offert l'opportunité de 
mettre en application mes connaissances dans un cadre professionnel enrichissant et réaliste.

Un remerciement particulier à mon encadrante académique pour sa coopération exemplaire et son 
accompagnement bienveillant. Sa disponibilité, ses conseils avisés et sa approche pédagogique ont 
joué un rôle déterminant dans l'aboutissement de ce projet. Grâce à son expertise et son soutien, 
j'ai pu surmonter les défis rencontrés et développer de précieuses compétences.

Je souhaite également exprimer ma sincère gratitude à mon encadrant professionnel, pour ses 
remarques pertinentes et son encadrement attentif, qui ont contribué à enrichir et structurer mon travail 
et à le rendre conforme aux réalités opérationnelles du secteur.

---

## Table des matières

- [Table des Figures](#table-des-figures)
- [Liste des Tableaux](#liste-des-tableaux)
- [Introduction Générale](#introduction-générale)

### Chapitres

1. [Contexte du projet](#chapitre-1--contexte-du-projet)
   - 1.1 Introduction
   - 1.2 Présentation de L'université
   - 1.3 Présentation de l'organisme d'accueil
   - 1.4 Étude de l'existant
   - 1.5 Méthodologie de travail et planification
   - 1.6 Étude de l'art
   - 1.7 Environnement de travail
   - 1.8 Conclusion

2. [Analyse des Besoins](#chapitre-2--analyse-des-besoins)
   - 2.1 Introduction
   - 2.2 Identification des acteurs
   - 2.3 Analyse des besoins
   - 2.4 Les Diagrammes
   - 2.5 Backlog du produit
   - 2.6 Modèle architectural
   - 2.7 Conclusion

3. [Authentification/Gestion des Utilisateurs](#chapitre-3--authentificationgestion-des-utilisateurs)
   - 3.1 Introduction
   - 3.2 Tableau Kanban
   - 3.3 Backlog du produit
   - 3.4 Les Diagrammes
   - 3.5 Réalisation
   - 3.6 Conclusion

4. [Gestion des Réservations et Chambres](#chapitre-4--gestion-des-réservations-et-chambres)
   - 4.1 Introduction
   - 4.2 Tableau Kanban
   - 4.3 Backlog du produit
   - 4.4 Les Diagrammes
   - 4.5 Réalisation
   - 4.6 Conclusion

5. [Gestion de la Maintenance et Tableau de Bord](#chapitre-5--gestion-de-la-maintenance-et-tableau-de-bord)
   - 5.1 Introduction
   - 5.2 Tableau Kanban
   - 5.3 Backlog du produit
   - 5.4 Les Diagrammes
   - 5.5 Réalisation
   - 5.6 Conclusion

- [Conclusion Générale](#conclusion-générale)
- [Webographie](#webographie)

---

## Table des Figures

1.1 Logo d'IT Business School (ITBS)  
1.2 Logo d'Hôtel Méditerranée  
1.3 Tableau Kanban pour la gestion des réservations  
1.4 Logo de Visual Studio Code  
1.5 Logo de Python  
1.6 Logo de Streamlit  
1.7 Logo de HTML/CSS/JavaScript  
1.8 Logo de Bootstrap  
1.9 Logo de SQLAlchemy  
1.10 Logo de PostgreSQL  
1.11 Logo de Postman  
1.12 Logo de Docker  
1.13 Logo de Git  
2.1 Diagramme de cas d'utilisation global  
2.2 Diagramme de classe global  
2.3 Architecture 3 tiers  
2.4 Architecture globale de l'application web  
2.5 Modèle d'architecture MVC  
3.1 Tableau Kanban - Authentification  
3.2 Diagramme des cas d'utilisation "Authentification"  
3.3 Diagramme des cas d'utilisation "Gestion Utilisateurs"  
3.4 Diagramme de séquence "Login"  
3.5 Diagramme de séquence "Register"  
3.6 Diagramme de séquence "Authentification"  
3.7 Diagramme de classe - Authentification  
3.10 Interface de connexion (Login)  
3.11 Formulaire d'inscription (Register)  
4.1 Tableau Kanban - Réservations  
4.2 Diagramme des cas d'utilisation "Réservations"  
4.3 Diagramme des cas d'utilisation "Gestion Chambres"  
4.4 Diagramme de séquence - Création réservation  
4.5 Diagramme de séquence - Gestion chambres  
4.6 Diagramme de classe - Réservations et Chambres  
4.7 Interface de gestion des réservations  
4.8 Interface de gestion des chambres  
5.1 Tableau Kanban - Maintenance et Tableau de Bord  
5.2 Diagramme des cas d'utilisation "Maintenance"  
5.3 Diagramme des cas d'utilisation "Tableau de Bord"  
5.4 Diagramme de séquence - Maintenance  
5.5 Diagramme de séquence - Tableau de Bord  
5.6 Diagramme de classe - Maintenance et Analyse  
5.7 Interface du tableau de bord principal  
5.8 Interface de gestion de la maintenance  

---

## Liste des Tableaux

1.1 Comparaison entre la approche Agile et approche classique  
1.2 Comparaison entre la méthode Agile et la méthode Kanban  
1.3 Comparaison entre les frameworks front-end  
1.4 Comparaison entre les langages de développement back-end  
1.5 Les caractéristiques des ordinateurs utilisés  
2.1 Backlog produit  
2.3 Acteurs et rôles  
3.1 Backlog Authentification/Gestion Utilisateurs  
3.2 Raffinement du cas d'utilisation "S'authentifier"  
3.3 Raffinement du cas d'utilisation "S'inscrire"  
3.4 Raffinement du cas d'utilisation "Gérer les Utilisateurs"  
4.1 Backlog Gestion des Réservations et Chambres  
4.2 Raffinement du cas d'utilisation "Gérer Réservations"  
4.3 Raffinement du cas d'utilisation "Gérer Chambres"  
5.1 Backlog Gestion de la Maintenance et Tableau de Bord  
5.2 Raffinement du cas d'utilisation "Gestion Maintenance"  
5.3 Raffinement du cas d'utilisation "Tableau de Bord"  

---

# Introduction Générale

Dans le secteur hôtelier, la gestion efficace des réservations, de la maintenance et du suivi operationnel 
constitue un enjeu crucial pour la qualité du service et la rentabilité de l'établissement. Les hôtels 
modernes, en particulier les petits et moyens établissements, sont confrontés à des défis quotidiens : 
gestion manuelle des réservations, suivi disparate de la maintenance, absence de vue d'ensemble sur 
l'occupation et la performance.

Ce projet s'inscrit dans cette dynamique en proposant une solution web intégrée de gestion hôtelière, 
spécialement conçue pour répondre aux besoins des hôtels côtiers, notamment en région méditerranéenne.

L'application permet de :
- Centraliser la gestion des réservations et des clients
- Automatiser le suivi des chambres et de leur disponibilité
- Gérer de manière structurée les tâches de maintenance
- Analyser les données d'occupation en temps réel
- Générer des rapports d'activité et de performance

Les hôtels sont souvent confrontés à une gestion désorganisée de leurs opérations, ce qui peut entraîner 
des erreurs de réservation, un suivi inefficace de la maintenance, une surcharge des employés, et une 
mauvaise prise de décision. En automatisant et en centralisant ces processus, notre solution vise à 
réduire les erreurs opérationnelles, améliorer la qualité du service client, optimiser l'utilisation des 
ressources, et faciliter la prise de décisions stratégiques basées sur des données fiables.

Grâce à une interface intuitive, des tableaux de bord en temps réel, des notifications intelligentes et 
un système sécurisé de gestion multi-utilisateurs, la plateforme permet à chaque établissement hôtelier 
d'avoir une gestion complète et cohérente de ses opérations quotidiennes.

En résumé, ce projet propose un outil moderne et évolutif de gestion hôtelière, intégrant des fonctionnalités 
avancées d'analyse de données, de notifications en temps réel et de reporting, afin d'aider les hôtels 
à optimiser leurs opérations et à renforcer leur compétitivité sur le marché touristique tunisien et international.

---

# Chapitre 1 : Contexte du projet

## 1.1 Introduction

Ce chapitre a pour mission de décrire le cadre général du projet. Il est consacré tout d'abord à la 
présentation de l'entreprise et de ses services. Par la suite, un sommaire sur la problématique ainsi 
que l'étude de l'existant. À la fin du chapitre, nous allons présenter la solution adoptée.

## 1.2 Présentation de L'université

**IT Business School (ITBS)** est une école d'ingénieurs privée située à Nabeul, créée en 2014. Elle 
permet à ses étudiants d'obtenir des diplômes d'ingénieur, de licence et de master dans les domaines 
de l'informatique et de la gestion. ITBS propose une large sélection de programmes de formation de 
qualité, adaptés aux profils et aux niveaux de compétence variés.

L'école s'engage à former des ingénieurs compétents et innovants, capables de relever les défis 
du marché du travail. Avec ses partenariats industriels et ses laboratoires modernes, ITBS offre 
une formation pratique et théorique de haut niveau, favorisant l'entrepreneuriat et l'innovation 
technologique.

---

### Figure 1.1: Logo d'IT Business School (ITBS)

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│               [Logo ITBS - À insérer ici]                   │
│                                                              │
│         École Supérieure des Technologies                   │
│       Information et Management de Nabeul                   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Description** : Le logo d'ITBS représente l'engagement de l'école envers l'excellence dans 
l'enseignement supérieur et la formation d'ingénieurs innovants pour le secteur des technologies 
de l'information et de la gestion.

---

## 1.3 Présentation de l'organisme d'accueil

### 1.3.1 Présentation générale d'Hôtel Méditerranée Nabeul

Cette section est dédiée à une présentation de l'entreprise hôte, Hôtel Méditerranée Hammamet, 
établissement emblématique du tourisme côtier tunisien offrant une expérience hôtelière de qualité supérieure.

---

### Figure 1.2: Logo d'Hôtel Méditerranée Nabeul

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│          [Logo Hôtel Méditerranée - À insérer ici]          │
│                                                              │
│           HÔTEL MÉDITERRANÉE NABEUL                         │
│      Côte Méditerranéenne Tunisienne                        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Description** : Le logo représente l'identité de marque de l'hôtel, reflétant son ancrage 
dans la région méditerranéenne et son engagement envers la qualité du service et l'accueil.

---

#### 1.3.1.1 Historique

Fondé en 1998, Hôtel Méditerranée Nabeul s'est imposé comme l'un des établissements hôteliers 
de référence sur la côte méditerranéenne tunisienne. Avec plus de deux décennies d'expérience, 
l'hôtel s'est construit une solide réputation en matière d'accueil, de qualité de service et de respect 
de l'environnement côtier.

Dès ses débuts, l'établissement s'est distingué par son engagement envers l'excellence. Au fil des 
années, l'hôtel a connu plusieurs phases de modernisation et d'expansion, renforçant ainsi son 
statut de destination touristique prisée. Son positionnement stratégique sur la corniche de Nabeul 
et ses vues panoramiques sur la mer Méditerranée en font un lieu idéal pour les touristes en quête 
de détente et de confort. L'hôtel dispose actuellement de 45 chambres réparties sur 5 étages, 
offrant une gamme complète de services et d'équipements modernes.

#### 1.3.1.2 Activités d'Hôtel Méditerranée

Hôtel Méditerranée propose une offre diversifiée de services :

- **Hébergement** : Chambres confortables avec vue mer, équipées de toutes les commodités modernes
- **Restauration** : Restaurant principal, bar de plage, service de room service
- **Loisirs et divertissements** : Piscine, spa, animations quotidiennes, plage privée
- **Services additionnels** : Réception 24h/24, conciergerie, parking, WiFi gratuit
- **Événements et séminaires** : Salles de conférence, organisation d'événements professionnels et familiaux

#### 1.3.1.3 Hôtel Méditerranée Nabeul

Situé à l'Avenue de la Corniche, 8000 Nabeul, Hôtel Méditerranée est un établissement à taille 
humaine avec 45 chambres, dominé par une direction engagée dans l'innovation et l'amélioration 
continue. L'hôtel s'engage à fournir des services de qualité tout en optimisant ses opérations 
internes par l'adoption de technologies modernes.

## 1.4 Étude de l'existant

Cette section évalue la situation actuelle chez Hôtel Méditerranée Nabeul, en identifiant les défis 
et les opportunités existants dans la gestion des opérations hôtelières.

### 1.4.1 Cadre général du projet

Notre stage s'est déroulé au sein d'Hôtel Méditerranée Nabeul dans le cadre de la réalisation de notre 
projet de fin d'études à l'Ecole Supérieure Privée des Technologies de l'Information et de Management 
de Nabeul (ITBS).

Ce projet consiste principalement à développer une application web de gestion hôtelière intégrée, 
permettant à l'établissement d'optimiser la gestion de ses réservations, de ses chambres, de ses 
clients et de la maintenance. L'application vise à offrir un suivi en temps réel des opérations grâce 
à des tableaux de bord dynamiques, à centraliser les données clients, et à faciliter la gestion de 
la maintenance des équipements et des services.

### 1.4.2 Solution actuelle

Actuellement, la gestion opérationnelle d'Hôtel Méditerranée repose principalement sur :

- Des outils bureautiques classiques (Excel, Word, email)
- Un système de réservation basique et déconnecté des autres opérations
- Des registres papier pour le suivi de la maintenance
- Une communication dispersée entre les départements
- Absence de tableau de bord centralisé de performance

Cette approche présente plusieurs limites :

- **Manque de visibilité en temps réel** : L'équipe n'a pas une vue d'ensemble instantanée du taux 
d'occupation, de l'état des chambres et des tâches en attente
- **Inefficacité opérationnelle** : Les processus manuels sont chronophages et sujets à erreurs
- **Communication fragmentée** : Les informations circulent difficilement entre la réception, 
l'entretien et l'administration
- **Absence de suivi des performances** : Pas de rapports fiables sur l'occupation, les revenus 
ou les indicateurs de satisfaction
- **Gestion inadaptée de la maintenance** : Les pannes et interventions ne sont pas suivies 
de manière structurée

### 1.4.3 Critique de l'existant

Pour mettre en place une solution efficace, il est essentiel d'analyser les faiblesses des systèmes 
existants et leurs impacts sur la gestion opérationnelle.

- **Absence de coordination centralisée** : Les systèmes actuels ne permettent pas une 
synchronisation en temps réel entre les différents départements
- **Perte d'informations critiques** : Les données sont dispersées et difficiles à récupérer 
pour l'analyse ou le reporting
- **Manque de sécurité et d'accessibilité** : Les données ne sont pas protégées adéquatement 
et les utilisateurs n'y accèdent pas facilement
- **Inefficacité du suivi de maintenance** : Les pannes et interventions ne sont pas priorisées 
et peuvent s'accumuler sans résolution
- **Faible accessibilité et ergonomie** : Les utilisateurs ne disposent pas d'une interface 
intuitive leur permettant de consulter rapidement les informations opérationnelles

En résumé, le système actuel de gestion hôtelière manque de fluidité et de modernisation, ce qui 
limite la réactivité et l'efficacité de l'établissement. L'objectif de ce projet est de concevoir une 
plateforme web intuitive et dynamique, offrant une vue centralisée et en temps réel de toutes les 
opérations hôtelières.

### 1.4.4 Solution proposée

Pour résoudre les problèmes identifiés dans la gestion opérationnelle d'Hôtel Méditerranée, nous 
avons proposé une application web intégrée de gestion hôtelière.

Cette application est conçue pour permettre un suivi en temps réel des réservations, une gestion 
optimisée des chambres et de leur disponibilité, un contrôle efficace de la maintenance, ainsi qu'une 
centralisation des données clients et des indicateurs de performance.

L'application se compose de trois principaux modules :

- **Tableau de bord de suivi opérationnel** : Ce tableau de bord affiche en temps réel l'état 
de l'hôtel (taux d'occupation, revenus, chambres disponibles, tâches de maintenance). Grâce à 
des notifications intelligentes, l'équipe est alertée des événements importants (réservation, 
maintenance urgente, arrivée client).

- **Gestion intégrée des réservations et des chambres** : Ce module permet une centralisation 
complète des réservations, la gestion de l'état des chambres (disponible, occupée, maintenance), 
et une synchronisation automatique des informations. Chaque utilisateur dispose de rôles définis 
assurant la sécurité et la séparation des responsabilités.

- **Système de gestion de la maintenance** : Ce module permet de créer, suivre et résoudre les 
pannes et les tâches de maintenance. Un système de priorités assure que les problèmes critiques 
sont traités en priorité.

Grâce à cette solution, Hôtel Méditerranée pourra bénéficier d'une gestion plus efficace et plus 
transparente de ses opérations. L'automatisation de certaines tâches permettra de réduire le temps 
de traitement des demandes, améliorer la qualité du service client et assurer une meilleure 
organisation des ressources.

## 1.5 Méthodologie de travail et planification

### 1.5.1 Définition d'une méthodologie

Une méthodologie est un ensemble de principes, de techniques et de pratiques organisées de manière 
structurée pour mener à bien un projet ou une tâche spécifique. Elle fournit un cadre de travail et 
des directives pour planifier, exécuter, contrôler et évaluer les activités nécessaires à la réalisation 
des objectifs.

Il existe différentes méthodologies de gestion de projet, dont les plus courantes sont les méthodologies 
classiques et agiles.

Les méthodologies classiques adoptent une approche séquentielle et prédictive, avec une planification 
rigide et une communication descendante. Des exemples de méthodologies classiques incluent le 
modèle en cascade et le modèle en V. En revanche, les méthodologies agiles adoptent une approche 
itérative et adaptative, avec une planification itération par itération et une communication interactive 
favorisant la collaboration. Des exemples de méthodologies agiles sont :

- **Scrum** : se caractérise par son approche itérative et collaborative, favorisant la livraison 
continue de fonctionnalités de haute qualité et il se base sur des cycles itératifs appelés "sprints".
- **DMAIC** : cette méthode se concentre sur l'amélioration continue des processus en suivant cinq 
étapes : Définir, Mesurer, Analyser, Améliorer et Contrôler.
- **Extreme Programming "XP"** : met l'accent sur la qualité du logiciel et la collaboration 
étroite entre les membres de l'équipe.

Dans le cadre de notre projet de fin d'études d'une durée de six mois, notre équipe de travail 
(encadrant et opérateurs) a choisi d'adopter une approche agile en utilisant la méthodologie Kanban.

### 1.5.2 Comparaison entre méthode Agile et méthode classique

| Critère | Méthode Agile | Méthode Classique |
|---------|---------------|-------------------|
| Approche du projet | Itérative et incrémentale, avec des ajustements fréquents en fonction des retours. | Linéaire et séquentielle, chaque phase doit être terminée avant la suivante. |
| Flexibilité | Très flexible et réactive aux changements. | Moins flexible, modifications difficiles une fois une phase terminée. |
| Communication | Encourage la communication continue et la collaboration. | Communication formelle, limitée aux points de contrôle. |
| Livraison | Livraison progressive de fonctionnalités. | Livraison globale à la fin du projet. |

**Table 1.1: Comparaison entre la approche Agile et approche classique**

### 1.5.3 Comparaison entre méthodologies Agile et méthode Kanban

| Critère | Méthode Agile | Méthode Kanban |
|---------|---------------|-----------------|
| Cadence et Planification | Basée sur des sprints définis. | Flux continu, pas de sprints fixes. |
| Gestion des Priorités | Réévaluation et ajustement des priorités à la fin de chaque sprint. | Gestion continue des priorités selon l'urgence et la capacité. |
| Flexibilité | Adaptation à la fin de chaque sprint. | Continu, avec une grande flexibilité dans le traitement des tâches. |
| Limitation du travail | Limite implicite via la taille des sprints. | Limite explicite du WIP (Work In Progress). |

**Table 1.2: Comparaison entre la méthode Agile et la méthode Kanban**

### 1.5.4 Présentation de la méthode Kanban

Kanban est une méthodologie agile qui met l'accent sur la visualisation et la gestion efficace du flux 
de travail. Contrairement aux approches séquentielles classiques, Kanban permet une adaptation 
continue en fonction des besoins et des priorités changeantes. Il repose sur l'utilisation d'un tableau 
Kanban pour suivre les différentes étapes du processus, en limitant le travail en cours (WIP) afin 
d'optimiser l'efficacité et d'éviter les goulets d'étranglement.

Cette approche est particulièrement adaptée aux environnements nécessitant une grande flexibilité, 
comme la gestion des opérations hôtelières. En appliquant Kanban, il devient plus facile de suivre 
l'avancement des tâches, d'identifier rapidement les blocages et d'améliorer la coordination entre 
les différents intervenants du projet.

### 1.5.5 Cycle de vie de la méthode Kanban

Le cycle de vie de Kanban repose sur une gestion visuelle du flux de travail, permettant une amélioration 
continue et une adaptation flexible aux besoins du projet. Voici comment nous appliquons Kanban 
à notre projet :

- **Visualisation du flux de travail** : Mise en place d'un tableau Kanban numérique pour 
représenter les différentes étapes du traitement des tâches (ex. : À traiter, En cours, En test, Complété).

- **Limitation du travail en cours (WIP)** : Définition d'un nombre maximum de tâches pouvant 
être traitées simultanément afin d'éviter l'engorgement et d'améliorer la réactivité.

- **Gestion des priorités** : Classement des tâches en fonction de leur urgence et de leur impact 
sur le service, permettant un traitement optimal des opérations les plus critiques.

- **Suivi et amélioration continue** : Analyse régulière des performances du processus, identification 
des blocages et ajustement des règles de gestion pour améliorer l'efficacité du système.

**Figure 1.3: Tableau Kanban pour la gestion des réservations**

```
┌────────────────────────────────────────────────────────────────────────┐
│               TABLEAU KANBAN - GESTION DES RÉSERVATIONS               │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  À TRAITER          │   EN COURS        │   EN RÉVISION   │ COMPLÉTÉ │
│  ─────────────────  │  ──────────────   │  ──────────────  │ ───────  │
│  ┌─────────────┐   │  ┌─────────────┐  │  ┌──────────┐    │         │
│  │ Réserv. #1  │   │  │ Réserv. #3  │  │  │ Réserv.  │    │         │
│  │ Chambre 101 │   │  │ Maintenance │  │  │    #5    │    │         │
│  │ 25-27 avril │   │  │ Chambre 204 │  │  │ Verif    │    │         │
│  └─────────────┘   │  └─────────────┘  │  └──────────┘    │         │
│  ┌─────────────┐   │  ┌─────────────┐  │  ┌──────────┐    │         │
│  │ Réserv. #2  │   │  │ Check-in    │  │  │ Paiement │    │ ✓ OK    │
│  │ Chambre 102 │   │  │ Client 45   │  │  │ Confirmé │    │ Réserv  │
│  │ 26-29 avril │   │  │ 15:30       │  │  │ Attente  │    │   #4    │
│  └─────────────┘   │  └─────────────┘  │  └──────────┘    │         │
│  ┌─────────────┐   │  ┌─────────────┐  │                 │         │
│  │ Réserv. #6  │   │  │ Nettoyage   │  │                 │         │
│  │ Chambre 103 │   │  │ Chambre 103 │  │                 │         │
│  │ 28 avril    │   │  │ 10:00-11:30 │  │                 │         │
│  └─────────────┘   │  └─────────────┘  │                 │         │
│                    │                    │                 │         │
│  WIP Max: 6        │ WIP Max: 6        │ WIP Max: 3      │ Illim.  │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

**Description détaillée** : Ce tableau Kanban illustre le flux de travail complet pour la gestion 
des réservations et des opérations hôtelières connexes. Les colonnes représentent les différents 
états possibles d'une tâche (À traiter, En cours, En révision, Complété). Cette visualisation 
aide l'équipe à :
- Identifier les goulets d'étranglement dans le processus
- Équilibrer le travail entre les membres de l'équipe
- Prioriser les tâches critiques
- Maintenir un flux de travail efficace et régulier
- Limiter le travail en cours (WIP) pour optimiser la productivité

Les limites WIP (Work In Progress) assurent que chaque colonne n'est pas surcharger de tâches.

### 1.5.6 Outils de la méthode Kanban

L'approche Kanban s'appuie sur plusieurs outils et techniques permettant de suivre et d'améliorer 
le processus en continu.

- **Tableau Kanban** : Utilisation d'un tableau physique ou numérique pour organiser et visualiser 
les tâches en cours et leur progression.

- **Swimlanes** : Séparation des tâches en catégories distinctes afin d'optimiser la gestion des priorités.

- **Limitation du WIP (Work In Progress)** : Mise en place de règles pour éviter l'accumulation 
excessive de tâches en cours, garantissant un flux de travail équilibré.

- **Diagramme de flux cumulatif (CFD - Cumulative Flow Diagram)** : Permet de suivre la 
progression des tâches dans le temps et d'identifier les éventuels goulots d'étranglement.

- **Stand-up meetings** : Brèves réunions quotidiennes pour faire le point sur l'état du projet, 
identifier les problèmes et ajuster les priorités en temps réel.

Grâce à l'application de ces principes et outils, notre projet garantit une gestion fluide et efficace 
des opérations hôtelières, en minimisant les retards et en améliorant la transparence des processus.

## 1.6 Étude de l'art

L'idée ici est de faire une étude assez détaillée et une analyse comparative sur ce qui existe dans 
le marché pour nous aider à implémenter la solution proposée.

### 1.6.1 Technologies Web

Avant de plonger tête baissée dans un projet et pour une réalisation organisée et séparée facilitant 
ce processus, le développement est divisé en deux étapes qui seront abordées en collaboration rapprochée.

- **Front-End** : C'est la partie apparente d'une application web qui est accessible par les utilisateurs finaux.
- **Back-End** : C'est la partie invisible d'une application web qui n'est pas à la portée des utilisateurs finaux.

Cette isolation est l'un des facteurs influençant l'extensibilité du code, elle permet également de 
gagner du temps en réduisant les tâches des développeurs. De plus, il est inutile d'héberger le code 
sur le même serveur, ce qui modifie l'infrastructure et offre plus de liberté aux développeurs.

#### 1.6.1.1 Définition d'un framework

Un framework est un ensemble structuré de concepts, de composants logiciels et de bonnes pratiques 
qui fournit une base pour le développement d'applications. Il s'agit d'un cadre de travail ou d'une 
infrastructure qui facilite la création, l'organisation et la gestion de logiciels en fournissant une 
structure et des outils prédéfinis.

Un framework offre des fonctionnalités et des abstractions prêtes à l'emploi, ce qui permet aux 
développeurs de se concentrer sur la résolution des problèmes spécifiques de leur application plutôt 
que de développer des fonctionnalités de base à partir de zéro.

#### 1.6.1.2 Frameworks front-end

Streamlit, React et Vue.js sont des technologies couramment utilisées pour le développement front-end. 
React et Vue.js sont des frameworks JavaScript, tandis que Streamlit est un framework Python rapide 
pour créer des applications web. Le choix entre ces trois options peut être délicat, car chaque développeur 
a ses préférences et chaque projet a ses propres besoins.

| Critère | Streamlit | React | Vue.js |
|---------|-----------|-------|--------|
| Facilité d'utilisation | ✓ Très simple | ✗ Courbe d'apprentissage | ✓ Modérée |
| Performance | ✓ Bonne | ✓ Excellente | ✓ Bonne |
| Flexibilité | ✗ Limitée | ✓ Très flexible | ✓ Flexible |
| Temps de développement | ✓ Très rapide | ✗ Plus long | ✓ Rapide |
| Widgets prédéfinis | ✓ Nombreux | ✗ Aucun | ✗ Aucun |

**Table 1.3: Comparaison entre les frameworks front-end**

Pour notre projet, nous avons choisi **Streamlit** car il permet un développement très rapide d'applications 
web complexes avec une excellente ergonomie, tout en offrant une excellente intégration avec Python.

#### 1.6.1.3 Frameworks back-end

Les langages de programmation back-end sont variés et se concurrencent les uns aux autres. Pour 
faire le meilleur choix, il est judicieux de faire une recherche sur chaque langage.

| Aspect | Python | Node.js | PHP |
|--------|--------|---------|-----|
| **Avantages** | — Langage polyvalent et puissant — Excellente intégration avec Streamlit — Nombreuses bibliothèques | — Performance élevée — Non-bloquant par défaut — Bon pour les APIs temps réel | — Facile à déployer — Écosystème mature |
| **Inconvénients** | — Moins performant que Node.js — Plus lourd à déployer | — Courbe d'apprentissage — Écosystème fragmenté | — Moins flexible que Python — Moins d'outils modernes |

**Table 1.4: Comparaison entre les langages de développement back-end**

Après avoir effectué une analyse approfondie de nos besoins et en tenant compte de la nécessité d'une 
intégration fluide entre le front-end (Streamlit) et le back-end, nous avons décidé d'utiliser **Python** 
avec **SQLAlchemy** pour l'ORM. Ce choix garantit une cohérence technologique, une développement 
rapide et une excellente maintenabilité du code.

#### 1.6.1.4 Système de gestion de base de données

Un système de gestion de base de données est un logiciel qui permet de stocker, organiser, gérer et 
récupérer des données de manière structurée et efficace. Il fournit un ensemble de fonctionnalités et 
d'outils pour créer, modifier, interroger et administrer une base de données.

Pour notre projet, nous utilisons **PostgreSQL** pour sa robustesse, sa fiabilité et son excellente 
support des fonctionnalités avancées. PostgreSQL est un système relationnel mature et open-source 
qui offre une excellente scalabilité et performance.

### 1.6.2 Sécurité et Authentification

La sécurité des applications web est un enjeu majeur dans le développement logiciel. Pour assurer 
la protection des données et l'intégrité des utilisateurs, plusieurs mécanismes de sécurité ont été 
mis en place dans ce projet.

#### 1.6.2.1 Authentification et Gestion des Utilisateurs

L'authentification de l'application repose sur un système sécurisé de gestion des utilisateurs et de 
leurs rôles. Chaque utilisateur doit s'authentifier avec un email et un mot de passe stockés de manière 
sécurisée dans la base de données. Les mots de passe sont protégés grâce à l'algorithme de hachage 
bcrypt, empêchant leur stockage en clair.

Un système de rôles (ROLE_ADMIN, ROLE_RECEPTIONIST, ROLE_HOUSEKEEPER) permet de 
restreindre l'accès aux différentes sections de l'application en fonction des responsabilités de 
chaque utilisateur.

#### 1.6.2.2 Protection contre les Attaques Web

Pour renforcer la sécurité, plusieurs mécanismes ont été mis en place :

- **Protection CSRF** : Utilisation de tokens CSRF pour empêcher les attaques par falsification 
de requêtes intersites.
- **Validation des entrées** : SQLAlchemy ORM est utilisé pour éviter les injections SQL en 
sécurisant les requêtes vers la base de données.
- **Restrictions d'accès** : Les routes sensibles sont protégées par un système de permissions 
basé sur les rôles.
- **Chiffrement des données sensibles** : Les informations critiques sont chiffrées avant stockage.

#### 1.6.2.3 Sécurisation des Sessions et Connexions

L'application met en place une gestion sécurisée des sessions. Les sessions sont stockées côté serveur 
et sont associées à des cookies sécurisés. De plus, pour éviter les attaques de type session fixation, 
les sessions sont régénérées après chaque connexion.

Grâce à ces mesures, l'application garantit une protection efficace contre les menaces courantes 
tout en offrant un accès sécurisé aux utilisateurs.

## 1.7 Environnement de travail

Depuis la spécification des besoins jusqu'à la fin du développement de notre projet, tout un 
environnement matériel et logiciel a été employé que nous détaillons dans cette partie.

### 1.7.1 Environnement matériel

| Caractéristiques | Spécifications |
|------------------|-----------------|
| Modèle | HP Pavilion 15 |
| Version système | Windows 11 |
| Processeur | AMD RYZEN 5600H |
| Stockage | 512GB SSD |
| Mémoire | 24.0 Go RAM |

**Table 1.5: Les caractéristiques des ordinateurs utilisés**

### 1.7.2 Environnement de développement

#### 1.7.2.1 Front-end

Dans cette section, nous présentons les différentes technologies front-end qui ont été utilisées pour 
développer et mettre en œuvre l'interface utilisateur de l'application.

**Visual Studio Code** : Éditeur de code gratuit multiplateforme publié par Microsoft qui permet 
de coder rapidement. Utilisé pour coder dans n'importe quel langage de programmation, sans changer 
d'éditeur. VS Code supporte de nombreux langages, notamment Python, JavaScript, HTML, CSS, etc.

**Streamlit** : Framework Python révolutionnaire permettant de transformer rapidement des scripts 
Python en applications web interactives. Streamlit offre une syntaxe simple pour créer des interfaces 
utilisateur professionnelles sans nécessiter de connaissances approfondies en développement web.

**HTML/CSS/JavaScript** : Ensemble technologique fondamental du web. HTML définit la structure, 
CSS gère la présentation, et JavaScript ajoute l'interactivité côté client.

**Bootstrap** : Framework CSS open-source pour développer des sites web responsives et mobile-first. 
Il fournit des composants pré-stylisés et un système de grille flexible.

**Plotly** : Bibliothèque de visualisation de données interactive permettant de créer des graphiques 
et tableaux de bord d'une grande qualité visuelle.

#### 1.7.2.2 Back-end

Dans cette partie, nous présentons les différents composants du backend de notre application.

**Python** : Langage de programmation versatile et puissant, utilisé pour développer la logique 
applicative. Python offre une syntaxe claire et une excellente écosystème de bibliothèques.

**SQLAlchemy** : ORM (Object-Relational Mapping) pour Python permettant une interaction élégante 
avec les bases de données. SQLAlchemy facilite la gestion des modèles de données et des requêtes 
SQL complexes.

**PostgreSQL** : Système de gestion de base de données relationnel robuste et open-source. 
PostgreSQL offre une excellente scalabilité, fiabilité et support des fonctionnalités avancées.

**Redis** : Système de cache en mémoire utilisé pour améliorer la performance de l'application 
en stockant les données fréquemment accédées.

**Postman** : Outil complet pour tester et documenter des APIs REST. Il permet d'envoyer des 
requêtes HTTP, automatiser des tests et générer de la documentation.

**Docker** : Plateforme de containerisation permettant de packager l'application et ses dépendances 
dans des conteneurs isolés pour un déploiement cohérent.

**Git** : Système de contrôle de version distribuée permettant de gérer efficacement le code source 
et la collaboration entre développeurs.

## 1.8 Conclusion

Dans ce premier chapitre, nous avons présenté le contexte et les objectifs de notre projet, en mettant 
en avant les problématiques existantes et les améliorations apportées par notre solution. Nous avons 
également détaillé les choix technologiques et méthodologiques adoptés pour assurer une gestion 
efficace du développement.

Un point clé a été la mise en place d'une architecture sécurisée pour l'authentification et la protection 
des données, garantissant ainsi la fiabilité et l'intégrité du système. Nous avons également abordé 
les outils et techniques qui faciliteront la gestion des réservations, des chambres et de la maintenance 
de manière centralisée et efficace.

Dans le prochain chapitre, nous procéderons à une analyse approfondie des besoins, en définissant 
les acteurs du système, les fonctionnalités essentielles et les contraintes à respecter. Cette étape 
sera appuyée par des modèles et diagrammes pour structurer clairement la conception de l'application.

---

# Chapitre 2 : Analyse des Besoins

## 2.1 Introduction

Une étape importante de tout cycle de développement d'un site web ou d'un concept consiste à 
effectuer des recherches préliminaires : c'est l'étape d'analyse et de spécification des exigences qui 
forment la base de toute idée à développer.

Dans ce deuxième chapitre, les exigences fonctionnelles de l'application sont abordées, en décrivant 
les fonctionnalités ciblées et en précisant les acteurs impliqués. Les exigences non fonctionnelles 
sont également prises en compte afin d'éviter le développement de solutions insatisfaisantes.

Pour exprimer ces exigences de manière structurée, des tableaux détaillant le diagramme de cas 
d'utilisation et le diagramme de classe sont utilisés.

## 2.2 Identification des acteurs

Un acteur est une « entité » externe au système qui interagit avec ce dernier. Dans cette application, 
quatre acteurs principaux ont été identifiés, chacun jouant un rôle spécifique dans l'utilisation 
du système. L'application est conçue pour répondre aux besoins de ces acteurs, dont les rôles sont 
décrits ci-dessous :

| Acteur | Rôle |
|--------|------|
| **Administrateur** | Responsable de la gestion complète de l'application. Il peut gérer les utilisateurs, consulter tous les rapports, configurer les paramètres système et superviser l'ensemble des fonctionnalités. |
| **Réceptionniste** | Gère les réservations, enregistre les clients, traite les check-in et check-out, et assure le suivi des demandes spéciales. |
| **Agent d'Entretien** | Responsable de l'entretien et de la maintenance des chambres. Il consulte les tâches assignées, met à jour l'état des chambres et signale les problèmes. |
| **Gérant de l'Hôtel** | Supervise les opérations générales, analyse les rapports de performance et prend les décisions stratégiques. |

**Table 2.3: Acteurs et rôles**

## 2.3 Analyse des besoins

Il est essentiel de mener une recherche approfondie et de collecter des données sur les fonctionnalités 
de base du système. En parallèle, l'analyse des interactions entre le système et les différents utilisateurs 
permet de déterminer avec précision les besoins fonctionnels et non fonctionnels de ce projet.

Cette démarche aide à recueillir des informations pertinentes sur les attentes des utilisateurs et à 
établir une base solide pour le développement de l'application.

### 2.3.1 Besoins fonctionnels

Les besoins fonctionnels constituent la base du système et définissent les actions essentielles que 
l'application doit être capable d'exécuter pour répondre aux attentes des utilisateurs. Dans le cadre 
de cette application de gestion hôtelière, les besoins fonctionnels couvrent les tâches suivantes :

- **Gérer les réservations** : Les utilisateurs peuvent créer, modifier, annuler et consulter les 
réservations. Le système doit valider la disponibilité des chambres et gérer les conflits.

- **Gérer les chambres** : Le système doit permettre de consulter, ajouter, modifier les chambres, 
gérer leur état (disponible, occupée, en maintenance) et synchroniser ces informations avec 
les réservations.

- **Gérer les clients** : Les utilisateurs peuvent enregistrer les nouveaux clients, mettre à jour 
leurs informations, consulter l'historique des réservations et gérer les préférences.

- **Suivi de la maintenance** : Le système permet de créer des rapports de pannes, d'assigner des 
tâches de maintenance, de suivre leur progression et d'archiver les interventions résolues.

- **Tableau de bord en temps réel** : Un tableau de bord dynamique affiche les indicateurs clés 
(taux d'occupation, revenus estimés, tâches en attente, pannes signalées).

- **Notifications intelligentes** : Le système envoie des notifications push pour les événements 
importants (nouvelle réservation, check-in à venir, maintenance urgente).

- **Rapports et statistiques** : Génération de rapports détaillés sur l'occupation, les revenus, 
la performance de l'établissement.

- **Gestion des utilisateurs** : L'administrateur peut créer, modifier ou supprimer des comptes 
utilisateurs, gérer leurs rôles et permissions.

### 2.3.2 Besoins non fonctionnels

En plus des fonctionnalités principales, il est essentiel de prendre en considération plusieurs besoins 
non fonctionnels afin de garantir une application performante, sécurisée et facile à utiliser.

- **Confidentialité et Sécurité** :
  - Authentification sécurisée avec gestion des rôles (administrateur, réceptionniste, entretien, gérant)
  - Accès restreint aux données par utilisateur (isolation des données)
  - Protection contre les attaques courantes (CSRF, injection SQL)
  - Chiffrage des mots de passe avec bcrypt
  - Sessions sécurisées avec expiration

- **Performance** :
  - Temps de réponse courts (< 1 seconde) pour le chargement du tableau de bord
  - Opérations CRUD rapides sur les réservations et chambres
  - Cache des données fréquemment accédées
  - Gestion efficace des pics de charge

- **Disponibilité** :
  - L'application doit être accessible 24h/24, 7j/7
  - Gestion appropriée des erreurs et tolérance aux pannes
  - Sauvegarde automatique des données

- **Ergonomie et Usabilité** :
  - Interface intuitive et responsive, adaptée aux différents appareils
  - Actions fréquentes rapidement accessibles
  - Design professionnel et conforme aux standards du web
  - Accessibilité pour les utilisateurs ayant des besoins spécifiques

- **Extensibilité** :
  - Architecture modulaire permettant l'ajout de nouvelles fonctionnalités
  - Intégration potentielle avec systèmes externes (PMS, systèmes de paiement)
  - API RESTful pour faciliter les intégrations futures

- **Fiabilité et Maintenabilité** :
  - Tests automatisés pour valider les fonctionnalités critiques
  - Code bien documenté et suivant les bonnes pratiques
  - Versioning du code avec Git pour tracer les modifications

## 2.4 Les Diagrammes

Les diagrammes UML (Unified Modeling Language) jouent un rôle essentiel dans la conception et 
la documentation de notre système. Ils nous permettent de représenter visuellement les différents 
aspects de l'architecture, des fonctionnalités et des interactions au sein de l'application.

### 2.4.1 Diagramme de cas d'utilisation global

Le diagramme de cas d'utilisation global illustre les différents acteurs du système et les interactions 
qu'ils peuvent avoir avec l'application. Il permet d'avoir une vision claire des fonctionnalités principales 
accessibles selon les rôles. Ce diagramme constitue un élément fondamental de la modélisation UML 
et guide le développement des modules.

---

### Figure 2.1: Diagramme de cas d'utilisation global

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SYSTÈME DE GESTION HÔTELIÈRE                             │
│                                                                             │
│  Admin        │                     Réceptionniste                     │ Gér │
│    │          │                           │                            │  │  │
│    ├──────┬───┼──────────────────────┬────┼────────────────┬──────────┼──┤  │
│    │      │   │                      │    │                │          │  │  │
│    │  ┌───▼──────────────────────────┴────────────────────┴──────────┐│  │  │
│    │  │  ┌──────────────────────────────────────────────┐            ││  │  │\n│    │  │  │   AUTHENTIFICATION & GESTION UTILISATEURS  │            ││  │  │\n│    │  │  │   - Connexion                               │            ││  │  │\n│    │  │  │   - Créer utilisateur                       │            ││  │  │\n│    │  │  │   - Gérer rôles et permissions              │            ││  │  │\n│    │  │  └──────────────────────────────────────────────┘            ││  │  │\n│    │  │                                                                ││  │  │\n│    │  │  ┌──────────────────────────────────────────────┐            ││  │  │\n│    │  │  │   GESTION DES RÉSERVATIONS                  │            ││  │  │\n│    │  │  │   - Créer réservation                        │            ││  │  │\n│    │  │  │   - Modifier réservation                     │────────────┼┼──┤  │\n│    │  │  │   - Annuler réservation                      │            ││  │  │\n│    │  │  │   - Consulter disponibilité                 │            ││  │  │\n│    │  │  └──────────────────────────────────────────────┘            ││  │  │\n│    │  │                                                                ││  │  │\n│    │  │  ┌──────────────────────────────────────────────┐            ││  │  │\n│    │  │  │   GESTION DES CHAMBRES                      │            ││  │  │\n│    │  │  │   - Ajouter chambre                          │            ││  │  │\n│    │  │  │   - Gérer état chambre (libre/occupée)      │────────────┼┼──┤  │\n│    │  │  │   - Consulter historique                    │            ││  │  │\n│    │  │  │   - Gérer catégories                         │            ││  │  │\n│    │  │  └──────────────────────────────────────────────┘            ││  │  │\n│    │  │                                                                ││  │  │\n│    │  │  ┌──────────────────────────────────────────────┐            ││  │  │\n│    │  │  │   GESTION DE LA MAINTENANCE                 │            ││  │  │\n│    │  │  │   - Signaler panne                           │────────────┼┼──┘  │\n│    │  │  │   - Assigner tâches                          │            ││     │\n│    │  │  │   - Mettre à jour statut                     │            ││     │\n│    │  │  │   - Consulter rapports                       │            ││     │\n│    │  │  └──────────────────────────────────────────────┘            ││     │\n│    │  │                                                                ││     │\n│    │  │  ┌──────────────────────────────────────────────┐            ││     │\n│    │  │  │   TABLEAU DE BORD & ANALYTIQUE              │            ││     │\n│    │  │  │   - Visualiser KPIs (occupancy, revenus)    │────────────┘│     │\n│    │  │  │   - Générer rapports                         │             │     │\n│    │  │  │   - Analyser données                         │             │     │\n│    │  │  │   - Notifications temps réel                │             │     │\n│    └──┼──┘  - Filtrer par date/statut                   │             └─────┘\n│       │     └──────────────────────────────────────────────┘                │\n│       │                                                                      │\n│       └──────────────────────────────────────────────────────────────────────┘\n│                                                                             │\n└─────────────────────────────────────────────────────────────────────────────┘\n```

**Description détaillée** : Ce diagramme UML illustre les interactions entre :
- **Administrateurs** : gestion complète du système (utilisateurs, configuration, rapports)
- **Réceptionnistes** : gestion des réservations et information clients
- **Agents d'Entretien** : suivi des tâches de maintenance et signalements de pannes
- **Gérants** : analyse de performance et prise de décisions stratégiques

Chaque acteur a accès aux modules qui correspondent à ses responsabilités.

---

### 2.4.2 Diagramme de classe global

Un diagramme de classes dans le langage de modélisation unifié (UML) est un type de diagramme 
de structure statique qui décrit la structure d'un système en montrant les classes du système, leurs 
attributs, les opérations (ou méthodes) et les relations entre les objets. C'est un élément essentiel 
de la modélisation qui guide l'implémentation.

---

### Figure 2.2: Diagramme de classe global

```
┌────────────────────────┐
│       << Class >>      │
│        USER            │
├────────────────────────┤
│ - id: Integer          │
│ - email: String        │
│ - password: String     │
│ - nom: String          │
│ - prenom: String       │
│ - role: Role           │
│ - active: Boolean      │
│ - created_at: DateTime │
│ - last_login: DateTime │
├────────────────────────┤
│ + login(email, pwd)    │
│ + logout()             │
│ + change_password()    │
│ + get_permissions()    │
└────────────────────────┘
         △ │
         │ │ has_role
    ┌────┘ └────┐
    │           │
┌───┴──────┐  ┌─┴────────────┐
│  ROLE    │  │ RESERVATION  │
├──────────┤  ├──────────────┤
│ -id      │  │ -id          │
│ -name    │  │ -user_id     │
│ -perms   │  │ -room_id     │
├──────────┤  │ -client_id   │
│ +getName │  │ -check_in    │
└──────────┘  │ -check_out   │
              │ -status      │
              ├──────────────┤
              │ +create()    │
              │ +update()    │
              │ +cancel()    │
              └──────────────┘
                     △ │
                     │ │ includes
           ┌─────────┘ └──────────┐
           │                      │
    ┌──────┴────────┐      ┌──────┴──────┐
    │     ROOM      │      │    CLIENT   │
    ├───────────────┤      ├─────────────┤
    │ -id           │      │ -id         │
    │ -number       │      │ -nom        │
    │ -category     │      │ -email      │
    │ -capacity     │      │ -phone      │
    │ -status       │      │ -address    │
    ├───────────────┤      ├─────────────┤
    │ +getStatus()  │      │ +add()      │
    │ +setStatus()  │      │ +update()   │
    │ +getHistory() │      │ +delete()   │
    └───────────────┘      └─────────────┘
           △                       
           │ related_to           
    ┌──────┴────────────┐
    │                   │
┌───┴──────────┐   ┌────┴────────────┐
│ MAINTENANCE  │   │   NOTIFICATION   │
├──────────────┤   ├──────────────────┤
│ -id          │   │ -id              │
│ -room_id     │   │ -user_id         │
│ -issue_type  │   │ -type            │
│ -priority    │   │ -message         │
│ -status      │   │ -created_at      │
│ -assigned_to │   │ -read_at         │
├──────────────┤   ├──────────────────┤
│ +create()    │   │ +send()          │
│ +update()    │   │ +mark_read()     │
│ +complete()  │   │ +delete()        │
└──────────────┘   └──────────────────┘
```

**Description détaillée** : Ce diagramme montre :
- **User** : classe centrale représentant les utilisateurs du système avec leurs attributs et opérations
- **Role** : gestion des rôles et permissions d'accès
- **Reservation** : ensemble des données et opérations liées aux réservations
- **Room** : gestion des chambres et de leur état
- **Client** : informations sur les clients de l'hôtel
- **Maintenance** : suivi des tâches de maintenance et pannes
- **Notification** : système de notifications en temps réel

Les relations entre les classes définissent comment elles interagissent.

---

## 2.5 Backlog du produit

Le backlog du produit est une liste ordonnée de toutes les fonctionnalités, améliorations et corrections 
nécessaires pour développer et livrer notre application web de gestion hôtelière.

| Acteur | User Story | Complexité | Priorité |
|--------|------------|-----------|----------|
| Administrateur | En tant qu'administrateur, je dois m'authentifier afin d'accéder à mon espace d'administration. | Moyenne | Forte |
| Administrateur | En tant qu'administrateur, je peux ajouter, modifier ou supprimer des utilisateurs. | Moyenne | Forte |
| Administrateur | En tant qu'administrateur, je peux consulter tous les rapports d'activité et les statistiques. | Forte | Forte |
| Réceptionniste | En tant que réceptionniste, je dois m'authentifier afin d'accéder à l'application. | Moyenne | Forte |
| Réceptionniste | En tant que réceptionniste, je peux créer, modifier ou annuler une réservation. | Moyenne | Forte |
| Réceptionniste | En tant que réceptionniste, je peux enregistrer un nouveau client. | Moyenne | Moyenne |
| Réceptionniste | En tant que réceptionniste, je peux effectuer le check-in et check-out des clients. | Moyenne | Forte |
| Réceptionniste | En tant que réceptionniste, je peux consulter la disponibilité des chambres en temps réel. | Faible | Forte |
| Agent Entretien | En tant qu'agent d'entretien, je peux consulter les tâches assignées. | Moyenne | Forte |
| Agent Entretien | En tant qu'agent d'entretien, je peux signaler une panne ou un problème. | Moyenne | Forte |
| Agent Entretien | En tant qu'agent d'entretien, je peux mettre à jour l'état d'une tâche de maintenance. | Moyenne | Forte |
| Gérant | En tant que gérant, je peux consulter le tableau de bord avec les indicateurs clés. | Moyenne | Forte |
| Gérant | En tant que gérant, je peux générer et télécharger les rapports de performance. | Forte | Moyenne |

**Table 2.1: Backlog produit**

## 2.6 Modèle architectural

Dans cette partie, nous allons présenter l'architecture sur laquelle repose notre application web 
et qui sera prise en compte lors de la conception des différents modules.

### 2.6.1 Architecture 3 tiers

L'architecture 3 tiers est un modèle d'organisation logicielle et d'infrastructure qui divise une 
application en trois parties distinctes :

- **Le tier de présentation ou « tier client »** : C'est la couche visible de l'application avec laquelle 
les utilisateurs interagissent. Il s'agit de l'interface utilisateur (UI) et de la logique de présentation. 
Ce tier est responsable de la collecte des entrées de l'utilisateur et de l'affichage des résultats 
ou des données demandées.

- **Le tier de logique métier ou « tier applicatif »** : Il s'agit de la couche intermédiaire qui traite 
les règles métier et la logique de l'application. Ce tier est responsable de la manipulation des 
données, de l'exécution des opérations métier et de la coordination entre le tier de présentation 
et le tier de données.

- **Le tier de données ou « tier serveur »** : C'est la couche inférieure qui stocke et gère les données 
de l'application. Il peut s'agir d'une base de données, d'un système de fichiers ou de tout autre 
moyen de stockage. Ce tier est responsable de l'accès aux données, de leur persistance et de leur 
récupération lorsque nécessaire.

**Figure 2.3: Architecture 3 tiers**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ARCHITECTURE 3 TIERS                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     TIER DE PRÉSENTATION                             │   │
│  │                     (Client / Frontend)                              │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │   │
│  │  │  Streamlit UI   │  │  HTML/CSS/JS    │  │  Plotly Charts  │     │   │
│  │  │  Interface Web  │  │  Composants     │  │  Visualisations │     │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘     │   │
│  └─────────────────────────────┬───────────────────────────────────────┘   │
│                                │ HTTP/REST                                 │
│                                ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     TIER LOGIQUE MÉTIER                              │   │
│  │                     (Application / Backend)                          │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │   │
│  │  │  Python Scripts │  │  Authentification│  │  Gestionnaire   │     │   │
│  │  │  Streamlit Logic│  │  Session/Query   │  │  Notifications  │     │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘     │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │   │
│  │  │  Chambre CRUD   │  │  Maintenance     │  │  Rapports       │     │   │
│  │  │  Réservations   │  │  Pannes/Composants│  │  Analytics      │     │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘     │   │
│  └─────────────────────────────┬───────────────────────────────────────┘   │
│                                │ SQLAlchemy / Pandas                       │
│                                ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     TIER DE DONNÉES                                  │   │
│  │                     (Persistence / Serveur)                          │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │   │
│  │  │  utilisateurs.  │  │  chambres.      │  │  maintenance_   │     │   │
│  │  │  json           │  │  csv            │  │  tasks.csv      │     │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘     │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │   │
│  │  │  notifications. │  │  pannes.        │  │  composants_    │     │   │
│  │  │  json           │  │  csv            │  │  chambres.csv   │     │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘     │   │
│  │  ┌─────────────────┐  ┌─────────────────┐                          │   │
│  │  │  rapports_      │  │  reclamations.  │                          │   │
│  │  │  taches.csv     │  │  csv            │                          │   │
│  │  └─────────────────┘  └─────────────────┘                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Description** : L'architecture 3 tiers sépare clairement les responsabilités :
- **Tier Présentation** : Interface Streamlit avec thème sombre, composants interactifs et tableaux de bord
- **Tier Logique** : Scripts Python gérant l'authentification, les opérations CRUD, les notifications en temps réel et les règles métier
- **Tier Données** : Fichiers CSV et JSON pour le stockage persistant des chambres, utilisateurs, tâches de maintenance, pannes, composants et réclamations

Cette architecture permet de séparer les préoccupations et de rendre l'application plus modulaire
et évolutive. Chaque tier peut être développé, déployé et mis à l'échelle indépendamment des autres, 
ce qui facilite la maintenance, les mises à jour et les améliorations de l'application dans son ensemble.

### 2.6.2 Architecture de l'application

Pour bien comprendre l'architecture et la dynamique de notre application web, nous allons exposer 
des schémas explicatifs des différentes parties du travail.

#### 2.6.2.1 Architecture globale

La figure 2.4 offre une vision détaillée de l'architecture frontend et backend de l'application web.

**Figure 2.4: Architecture globale de notre application web**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ARCHITECTURE GLOBALE DE L'APPLICATION                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌──────────────────────┐         ┌──────────────────────┐                │
│   │   UTILISATEUR        │         │   UTILISATEUR        │                │
│   │   (Admin/Réception/  │         │   (Agent Maintenance)│                │
│   │   Gérant)            │         │                      │                │
│   └──────────┬───────────┘         └──────────┬───────────┘                │
│              │ HTTP Request                    │ HTTP Request               │
│              ▼                                ▼                            │
│   ┌──────────────────────────────────────────────────────┐                │
│   │              STREAMLIT FRONTEND                       │                │
│   │  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  │                │
│   │  │ show_login()│  │show_main_app│  │  Sidebar     │  │                │
│   │  │   (Auth)    │  │  (Dashboard)│  │  Navigation  │  │                │
│   │  └─────────────┘  └─────────────┘  └──────────────┘  │                │
│   │  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  │                │
│   │  │ Tabs Admin  │  │Tabs Récept. │  │ Tabs Maint.  │  │                │
│   │  │ 8 onglets   │  │ 2 onglets   │  │ 2 onglets    │  │                │
│   │  └─────────────┘  └─────────────┘  └──────────────┘  │                │
│   └────────────────────────┬─────────────────────────────┘                │
│                            │ st.session_state / QueryParams                │
│                            ▼                                               │
│   ┌──────────────────────────────────────────────────────┐                │
│   │              PYTHON BACKEND (app.py)                  │                │
│   │  ┌──────────────────────────────────────────────┐    │                │
│   │  │         MODULES DE GESTION                    │    │                │
│   │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐        │    │                │
│   │  │  │load_    │ │load_    │ │load_    │        │    │                │
│   │  │  │users()  │ │rooms()  │ │tasks()  │        │    │                │
│   │  │  └─────────┘ └─────────┘ └─────────┘        │    │                │
│   │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐        │    │                │
│   │  │  │load_    │ │load_    │ │load_    │        │    │                │
│   │  │  │pannes() │ │composants│ │rapports()       │    │                │
│   │  │  └─────────┘ └─────────┘ └─────────┘        │    │                │
│   │  └──────────────────────────────────────────────┘    │                │
│   │  ┌──────────────────────────────────────────────┐    │                │
│   │  │      SERVICES TECHNIQUES                      │    │                │
│   │  │  ┌─────────────┐  ┌─────────────────────┐   │    │                │
│   │  │  │authenticate │  │add_notification()   │   │    │                │
│   │  │  │hash_password│  │play_notification_   │   │    │                │
│   │  │  │is_admin()   │  │sound()              │   │    │                │
│   │  │  └─────────────┘  └─────────────────────┘   │    │                │
│   │  │  ┌─────────────┐  ┌─────────────────────┐   │    │                │
│   │  │  │check_and_   │  │get_tabs_for_role()  │   │    │                │
│   │  │  │restore_     │  │navigate_to_tab()    │   │    │                │
│   │  │  │session()    │  │                     │   │    │                │
│   │  │  └─────────────┘  └─────────────────────┘   │    │                │
│   │  └──────────────────────────────────────────────┘    │                │
│   └────────────────────────┬─────────────────────────────┘                │
│                            │ pandas.read_csv / to_csv                      │
│                            │ json.load / json.dump                         │
│                            ▼                                               │
│   ┌──────────────────────────────────────────────────────┐                │
│   │              COUCHE DE DONNÉES (CSV/JSON)             │                │
│   │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐  │                │
│   │  │utilisateurs. │ │  chambres.   │ │maintenance_  │  │                │
│   │  │    json      │ │    csv       │ │  tasks.csv   │  │                │
│   │  └──────────────┘ └──────────────┘ └──────────────┘  │                │
│   │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐  │                │
│   │  │notifications.│ │   pannes.    │ │composants_   │  │                │
│   │  │    json      │ │    csv       │ │chambres.csv  │  │                │
│   │  └──────────────┘ └──────────────┘ └──────────────┘  │                │
│   │  ┌──────────────┐ ┌──────────────┐                   │                │
│   │  │ rapports_    │ │reclamations. │                   │                │
│   │  │ taches.csv   │ │    csv       │                   │                │
│   │  └──────────────┘ └──────────────┘                   │                │
│   └──────────────────────────────────────────────────────┘                │
│                                                                             │
│   Légende: ────► Flux de données / Requêtes                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Description** : Ce schéma détaille l'architecture globale avec :
- **Streamlit Frontend** : Interface adaptative avec onglets différenciés selon le rôle (Admin: 8 onglets, Réception: 2 onglets, Maintenance: 2 onglets)
- **Python Backend** : Modules de gestion des données et services techniques (authentification, notifications, navigation)
- **Couche de Données** : Fichiers CSV et JSON pour la persistance locale

Le flux de communication fonctionne comme suit :

1. L'utilisateur interagit avec l'interface Streamlit
2. L'interface envoie une requête au serveur d'application
3. Le serveur traite la logique métier
4. Les données sont récupérées ou mises à jour dans PostgreSQL
5. La réponse est formatée et renvoyée à l'interface
6. L'interface se met à jour avec les nouvelles données

#### 2.6.2.2 Architecture Front-End

**Template** : Partie du composant affichée à l'utilisateur dans Streamlit, incluant les éléments UI

**Logique de présentation** : Code Python dans Streamlit qui gère l'affichage, les validations 
côté client et l'interaction avec l'utilisateur

**Service** : Module qui gère la communication avec le backend, en envoyant les requêtes et 
récupérant les réponses

#### 2.6.2.3 Architecture Back-End

L'architecture backend suit le pattern MVC (Modèle-Vue-Contrôleur) :

**Modèle** : Les classes représentant les entités métier (User, Reservation, Room, etc.) et leur 
interaction avec la base de données via SQLAlchemy

**Vue** : Représentée par les schémas de réponse qui structurent les données pour le frontend

**Contrôleur** : Les fonctions et classes qui traitent la logique métier, valident les entrées et 
orchestrent les opérations sur les modèles

**Figure 2.5: Modèle d'architecture MVC**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MODÈLE D'ARCHITECTURE MVC                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                         VUE (View)                                   │  │
│   │              Interface Utilisateur Streamlit                         │  │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │  │
│   │  │  st.title() │  │ st.metric() │  │st.dataframe()│  │st.sidebar()│ │  │
│   │  │  Titres     │  │  Indicateurs│  │  Tableaux   │  │ Navigation │ │  │
│   │  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘ │  │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │  │
│   │  │ st.button() │  │st.selectbox()│  │ st.form()   │                  │  │
│   │  │  Boutons    │  │  Listes     │  │  Formulaires│                  │  │
│   │  └─────────────┘  └─────────────┘  └─────────────┘                  │  │
│   └────────────────────────┬────────────────────────────────────────────┘  │
│                            │ Affichage / Interaction                        │
│                            ▼                                                │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                      CONTRÔLEUR (Controller)                         │  │
│   │              Logique Métier et Orchestration                         │  │
│   │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │  │
│   │  │  authenticate() │  │create_maintenance│  │update_room_    │     │  │
│   │  │  hash_password()│  │_task()          │  │status()         │     │  │
│   │  └─────────────────┘  └─────────────────┘  └─────────────────┘     │  │
│   │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │  │
│   │  │add_reclamation()│  │add_notification()│  │get_tabs_for_   │     │  │
│   │  │                 │  │play_notification_│  │role()           │     │  │
│   │  │                 │  │sound()           │  │                 │     │  │
│   │  └─────────────────┘  └─────────────────┘  └─────────────────┘     │  │
│   │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │  │
│   │  │check_and_restore│  │load_rooms()     │  │save_users()     │     │  │
│   │  │_session()       │  │load_tasks()     │  │delete_user()    │     │  │
│   │  └─────────────────┘  └─────────────────┘  └─────────────────┘     │  │
│   └────────────────────────┬────────────────────────────────────────────┘  │
│                            │ Traitement / Validation                        │
│                            ▼                                                │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                        MODÈLE (Model)                                │  │
│   │              Entités et Persistance des Données                      │  │
│   │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │  │
│   │  │   Utilisateur   │  │    Chambre      │  │ TacheMaintenance│     │  │
│   │  │  - username     │  │  - numero       │  │  - id           │     │  │
│   │  │  - password     │  │  - type         │  │  - chambre      │     │  │
│   │  │  - role         │  │  - statut       │  │  - statut       │     │  │
│   │  │  - nom          │  │  - aile/etage   │  │  - priorite     │     │  │
│   │  └─────────────────┘  └─────────────────┘  └─────────────────┘     │  │
│   │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │  │
│   │  │   Reclamation   │  │   Composant     │  │  Notification   │     │  │
│   │  │  - id           │  │  - id           │  │  - title        │     │  │
│   │  │  - chambre      │  │  - chambre      │  │  - message      │     │  │
│   │  │  - type_panne   │  │  - composant    │  │  - type         │     │  │
│   │  │  - statut       │  │  - statut       │  │  - target_role  │     │  │
│   │  └─────────────────┘  └─────────────────┘  └─────────────────┘     │  │
│   │  ┌─────────────────┐  ┌─────────────────┐                          │  │
│   │  │   TypePanne     │  │  RapportTache   │                          │  │
│   │  │  - nom_panne    │  │  - task_id      │                          │  │
│   │  │  - priorite     │  │  - agent        │                          │  │
│   │  │  - description  │  │  - rapport      │                          │  │
│   │  └─────────────────┘  └─────────────────┘                          │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│   Flux: Vue ◄──► Contrôleur ◄──► Modèle                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Description** : Le pattern MVC sépare l'application en trois composants :
- **Vue (View)** : Interface Streamlit qui présente les données et collecte les interactions utilisateur (boutons, formulaires, tableaux, métriques)
- **Contrôleur (Controller)** : Fonctions Python qui traitent la logique métier, valident les entrées et coordonnent les opérations entre la Vue et le Modèle
- **Modèle (Model)** : Entités de données représentées par les structures CSV/JSON (Utilisateur, Chambre, TâcheMaintenance, Réclamation, Composant, Notification, TypePanne, RapportTache)

Ce pattern assure une séparation claire des responsabilités et facilite la maintenance du code.

### 2.6.3 Pourquoi utiliser cette architecture

- **Développement simultané** : La séparation des composants permet à plusieurs développeurs 
de travailler en parallèle sur des parties différentes de l'application.

- **Réutilisation** : La présentation est séparée de la logique, permettant la réutilisation des 
composants avec des jeux de données différents.

- **Évolutivité accrue** : En cas de problèmes de performance, chaque couche peut être optimisée 
indépendamment.

- **Faible couplage** : Les connexions entre les modèles, vues et contrôleurs sont minimisées, 
réduisant les dépendances.

- **Meilleure extensibilité** : Les composants étant indépendants, les modifications peuvent être 
effectuées localement sans affecter l'ensemble de l'application.

## 2.7 Conclusion

En conclusion, cette analyse nous a permis de mieux comprendre les besoins et les exigences du 
système de gestion hôtelière, ainsi que les acteurs impliqués dans son utilisation. Nous avons pu 
identifier et définir de manière précise les fonctionnalités essentielles à intégrer, tout en prenant 
en compte les contraintes non fonctionnelles, telles que la sécurité, la performance, et la disponibilité, 
qui garantiront une expérience utilisateur optimale. Cette phase de spécification prépare le terrain 
pour une conception robuste et efficace.

La prochaine étape se concentrera sur les mécanismes d'authentification sécurisée et la gestion des 
utilisateurs.

---

# Chapitre 3 : Authentification/Gestion des Utilisateurs

## 3.1 Introduction

Ce chapitre explore les fonctionnalités centrales de l'authentification et de la gestion des utilisateurs, 
en s'appuyant sur les processus fondamentaux présentés précédemment. Nous commençons par détailler 
le workflow d'authentification dans notre tableau Kanban, suivi d'une analyse approfondie de la 
gestion des rôles et permissions.

## 3.2 Tableau Kanban

Le processus d'authentification est représenté par les fonctionnalités de connexion (login), d'inscription 
(register) et de gestion des utilisateurs (manage users), qui constituent les tâches en cours dans notre 
tableau Kanban.

**Figure 3.1: Tableau Kanban - Authentification**

```
┌────────────────────────────────────────────────────────────────────────┐
│            TABLEAU KANBAN - AUTHENTIFICATION & UTILISATEURS           │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  À TRAITER          │   EN COURS        │   EN TEST     │  COMPLÉTÉ  │
│  ─────────────────  │  ──────────────   │  ───────────  │  ────────  │
│  ┌─────────────┐   │  ┌─────────────┐  │  ┌─────────┐  │  ┌──────┐  │
│  │ Créer page  │   │  │ Implémenter │  │  │ Vérifier│  │  │Login │  │
│  │ login UI    │   │  │ hash bcrypt │  │  │ session│  │  │  OK  │  │
│  │             │   │  │ passwords   │  │  │ restore│  │  │      │  │
│  └─────────────┘   │  └─────────────┘  │  └─────────┘  │  └──────┘  │
│  ┌─────────────┐   │  ┌─────────────┐  │               │  ┌──────┐  │
│  │ Créer page  │   │  │ Gestion     │  │               │  │Reset │  │
│  │ register UI │   │  │ rôles       │  │               │  │password│ │
│  │             │   │  │ (admin/rec) │  │               │  │  OK  │  │
│  └─────────────┘   │  └─────────────┘  │               │  └──────┘  │
│  ┌─────────────┐   │                   │               │            │
│  │ Formulaire  │   │                   │               │            │
│  │ reset pwd   │   │                   │               │            │
│  └─────────────┘   │                   │               │            │
│  ┌─────────────┐   │                   │               │            │
│  │ Liste users │   │                   │               │            │
│  │ CRUD admin  │   │                   │               │            │
│  └─────────────┘   │                   │               │            │
│                    │                   │               │            │
│  WIP Max: 5        │ WIP Max: 3        │ WIP Max: 2    │ Illimité   │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

**Description** : Ce tableau Kanban illustre le flux de développement du module d'authentification avec :
- **À traiter** : Création des interfaces login/register, formulaire de réinitialisation, gestion des utilisateurs
- **En cours** : Implémentation du hachage bcrypt et gestion des rôles
- **En test** : Vérification de la restauration de session et persistance
- **Complété** : Fonctionnalités de connexion et réinitialisation de mot de passe validées

## 3.3 Backlog du produit - Authentification/Gestion Utilisateurs

| Acteur | User Story | Complexité | Priorité |
|--------|------------|-----------|----------|
| Administrateur | En tant qu'administrateur, je peux créer un nouveau compte utilisateur. | Moyenne | Forte |
| Administrateur | En tant qu'administrateur, je peux modifier les informations d'un utilisateur. | Moyenne | Moyenne |
| Administrateur | En tant qu'administrateur, je peux désactiver ou supprimer un utilisateur. | Moyenne | Moyenne |
| Administrateur | En tant qu'administrateur, je peux consulter l'historique des connexions. | Forte | Moyenne |
| Utilisateur | En tant qu'utilisateur, je peux me connecter avec mon email et mon mot de passe. | Moyenne | Forte |
| Utilisateur | En tant qu'utilisateur, je peux réinitialiser mon mot de passe oublié. | Forte | Forte |
| Utilisateur | En tant qu'utilisateur, ma session doit rester active lors de la navigation. | Moyenne | Forte |

**Table 3.1: Backlog Authentification/Gestion Utilisateurs**

## 3.4 Les Diagrammes

### 3.4.1 Diagramme des cas d'utilisation

**Figure 3.2: Diagramme des cas d'utilisation "Authentification"**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CAS D'UTILISATION - AUTHENTIFICATION                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Utilisateur                                                               │
│   (Non authentifié)                                                         │
│       │                                                                     │
│       │ Se connecter                                                        │
│       ├──────────────────────►┌─────────────────┐                          │
│       │                       │   S'authentifier │                          │
│       │                       │   - Saisir email │                          │
│       │                       │   - Saisir mdp   │                          │
│       │                       │   - Valider      │                          │
│       │                       └────────┬────────┘                          │
│       │                                │                                    │
│       │         ┌──────────────────────┼──────────────────────┐            │
│       │         │                      │                      │            │
│       │         ▼                      ▼                      ▼            │
│       │  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐        │
│       │  │  Identifiants│      │  Session    │      │  Redirection│        │
│       │  │  corrects    │      │  créée      │      │  Dashboard  │        │
│       │  └─────────────┘      └─────────────┘      └─────────────┘        │
│       │                                                                     │
│       │ Réinitialiser mot de passe                                          │
│       ├──────────────────────►┌─────────────────┐                          │
│       │                       │  Reset Password │                          │
│       │                       │  - Saisir email │                          │
│       │                       │  - Confirmer    │                          │
│       │                       └─────────────────┘                          │
│       │                                                                     │
│       │ ◄──────────────────────┐                                            │
│       │                        │                                            │
│   ┌───┴───┐              ┌─────┴─────┐                                      │
│   │ Admin  │              │  Système  │                                      │
│   └───┬───┘              └─────┬─────┘                                      │
│       │                        │                                            │
│       │ Créer utilisateur      │                                            │
│       ├──────────────────────►│                                            │
│       │                       │ Générer mot de passe temporaire             │
│       │ ◄──────────────────────┤                                            │
│       │                        │                                            │
│       │ Assigner rôle          │                                            │
│       ├──────────────────────►│                                            │
│       │                        │                                            │
│       │ ◄──────────────────────┤                                            │
│       │   Confirmation création│                                            │
│       │                        │                                            │
│                                                                             │
│   Légende: ────► Interaction principale                                    │
│            ─ ─ ► Interaction secondaire                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Description** : Ce diagramme illustre les cas d'utilisation du module d'authentification :
- **S'authentifier** : L'utilisateur saisit ses identifiants (email/mot de passe), le système valide et crée une session
- **Réinitialiser mot de passe** : L'utilisateur demande une réinitialisation, le système génère un nouveau mot de passe
- **Créer utilisateur** (Admin uniquement) : L'administrateur crée un compte, assigne un rôle, le système génère un mot de passe temporaire

Les scénarios d'exception incluent : identifiants incorrects, compte désactivé, email déjà utilisé.

#### Raffinement du cas d'utilisation "Login"

| Cas d'utilisation | Login |
|------------------|--------|
| **Acteur** | Utilisateur |
| **Pré-condition** | Interface de connexion affichée, utilisateur non authentifié |
| **Post-condition** | Utilisateur authentifié, session créée, redirection vers le tableau de bord |
| **Scénario nominal** | 1. L'utilisateur saisit son email<br>2. L'utilisateur saisit son mot de passe<br>3. L'utilisateur clique sur "Se connecter"<br>4. Le système valide les identifiants<br>5. Une session est créée<br>6. L'utilisateur est redirigé vers le tableau de bord |
| **Scénario d'exception** | • Identifiants incorrects → message d'erreur affiché<br>• Utilisateur désactivé → accès refusé<br>• Compte inexistant → message d'erreur |

**Table 3.2: Raffinement du cas d'utilisation "S'authentifier"**

#### Raffinement du cas d'utilisation "Register"

| Cas d'utilisation | Register (Inscription) |
|------------------|--------|
| **Acteur** | Administrateur (créant un compte pour un nouvel utilisateur) |
| **Pré-condition** | Administrateur connecté, formulaire de création d'utilisateur accessible |
| **Post-condition** | Nouveau compte créé, identifiants générés et communiqués |
| **Scénario nominal** | 1. L'administrateur accède au formulaire de création<br>2. Il remplit les informations de l'utilisateur<br>3. Il assigne un rôle (Admin, Receptionist, Housekeeper, Manager)<br>4. Un mot de passe temporaire est généré<br>5. Le compte est créé<br>6. L'utilisateur reçoit ses identifiants par email |
| **Scénario d'exception** | • Email déjà utilisé → erreur<br>• Informations manquantes → validation échouée<br>• Format d'email invalide → erreur |

**Table 3.3: Raffinement du cas d'utilisation "S'inscrire"**

**Figure 3.3: Diagramme des cas d'utilisation "Gestion Utilisateurs"**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                CAS D'UTILISATION - GESTION DES UTILISATEURS                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│     Admin                                                                   │
│       │                                                                     │
│       │ Consulter liste utilisateurs                                        │
│       ├──────────────────────►┌─────────────────────────────────┐          │
│       │                       │     Consulter Utilisateurs      │          │
│       │                       │     - Voir tableau users        │          │
│       │                       │     - Filtrer par rôle          │          │
│       │                       │     - Rechercher par nom        │          │
│       │                       └─────────────────────────────────┘          │
│       │                                                                     │
│       │ Créer utilisateur                                                   │
│       ├──────────────────────►┌─────────────────────────────────┐          │
│       │                       │     Créer Utilisateur           │          │
│       │                       │     - Saisir nom, email         │          │
│       │                       │     - Sélectionner rôle         │          │
│       │                       │     - Générer mot de passe      │          │
│       │                       │     - Confirmer création        │          │
│       │                       │                                 │          │
│       │ ◄──────────────────────┤                                 │          │
│       │   Confirmation création│                                 │          │
│       │                       └─────────────────────────────────┘          │
│       │                                                                     │
│       │ Modifier utilisateur                                              │
│       ├──────────────────────►┌─────────────────────────────────┐          │
│       │                       │     Modifier Utilisateur        │          │
│       │                       │     - Changer nom/email         │          │
│       │                       │     - Modifier rôle             │          │
│       │                       │     - Activer/Désactiver        │          │
│       │                       └─────────────────────────────────┘          │
│       │                                                                     │
│       │ Supprimer utilisateur                                             │
│       ├──────────────────────►┌─────────────────────────────────┐          │
│       │                       │     Supprimer Utilisateur       │          │
│       │                       │     - Confirmation              │          │
│       │                       │     - Suppression définitive    │          │
│       │                       └─────────────────────────────────┘          │
│       │                                                                     │
│       │ Réinitialiser mot de passe                                        │
│       ├──────────────────────►┌─────────────────────────────────┐          │
│       │                       │     Reset Password              │          │
│       │                       │     - Saisir email              │          │
│       │                       │     - Générer nouveau mdp       │          │
│       │                       │     - Afficher confirmation     │          │
│       │                       └─────────────────────────────────┘          │
│       │                                                                     │
│   ┌───┴───┐                                                                 │
│   │ Système│                                                                 │
│   └───┬───┘                                                                 │
│       │ Valider email unique                                                │
│       │ Vérifier format                                                     │
│       │ Hacher mot de passe (bcrypt)                                        │
│       │ Sauvegarder dans JSON                                               │
│       │                                                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Description** : Ce diagramme détaille les cas d'utilisation de gestion des utilisateurs, réservés à l'administrateur :
- **Consulter Utilisateurs** : Liste complète des utilisateurs avec filtres et recherche
- **Créer Utilisateur** : Formulaire de création avec génération automatique de mot de passe temporaire
- **Modifier Utilisateur** : Mise à jour des informations, changement de rôle, activation/désactivation
- **Supprimer Utilisateur** : Suppression définitive avec confirmation
- **Reset Password** : Génération d'un nouveau mot de passe pour un utilisateur existant

Les validations système incluent : vérification d'unicité de l'email, format valide, hachage bcrypt sécurisé.

### 3.4.2 Diagramme de séquence

**Figure 3.4: Diagramme de séquence "Login"**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DIAGRAMME DE SÉQUENCE - LOGIN                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Utilisateur          Interface           Backend           Fichier JSON   │
│      │                    │                   │                   │         │
│      │ 1. Saisir email    │                   │                   │         │
│      │───────────────────►│                   │                   │         │
│      │                    │                   │                   │         │
│      │ 2. Saisir password │                   │                   │         │
│      │───────────────────►│                   │                   │         │
│      │                    │                   │                   │         │
│      │ 3. Cliquer "Login" │                   │                   │         │
│      │───────────────────►│                   │                   │         │
│      │                    │                   │                   │         │
│      │                    │ 4. authenticate() │                   │         │
│      │                    │──────────────────►│                   │         │
│      │                    │                   │                   │         │
│      │                    │                   │ 5. load_users()   │         │
│      │                    │                   │──────────────────►│         │
│      │                    │                   │                   │         │
│      │                    │                   │ 6. Vérifier hash  │         │
│      │                    │                   │    bcrypt         │         │
│      │                    │                   │◄──────────────────│         │
│      │                    │                   │                   │         │
│      │                    │                   │ 7. Vérifier rôle  │         │
│      │                    │                   │    actif          │         │
│      │                    │                   │                   │         │
│      │                    │ 8. Session créée  │                   │         │
│      │                    │◄──────────────────│                   │         │
│      │                    │                   │                   │         │
│      │                    │ 9. Query params   │                   │         │
│      │                    │    update         │                   │         │
│      │                    │                   │                   │         │
│      │ 10. Redirection    │                   │                   │         │
│      │    Dashboard       │                   │                   │         │
│      │◄───────────────────│                   │                   │         │
│      │                    │                   │                   │         │
│      │ [Alt: Erreur]      │                   │                   │         │
│      │◄───────────────────│                   │                   │         │
│      │ "Identifiants      │                   │                   │         │
│      │  incorrects"       │                   │                   │         │
│      │                    │                   │                   │         │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Description** : Ce diagramme de séquence illustre le flux d'authentification :
1. L'utilisateur saisit son email et mot de passe dans l'interface Streamlit
2. L'interface appelle la fonction `authenticate()` du backend
3. Le backend charge les utilisateurs depuis le fichier JSON
4. Vérification du hash bcrypt du mot de passe
5. Vérification que le compte est actif et du rôle
6. Création de la session et mise à jour des query params
7. Redirection vers le tableau de bord avec les onglets appropriés au rôle

En cas d'erreur (identifiants incorrects, compte désactivé), un message d'erreur est affiché.

**Figure 3.5: Diagramme de séquence "Register"**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DIAGRAMME DE SÉQUENCE - REGISTER                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Admin              Interface             Backend           Fichier JSON   │
│    │                    │                   │                   │           │
│    │ 1. Accéder formulaire│                 │                   │           │
│    │─────────────────────►│                 │                   │           │
│    │                      │                 │                   │           │
│    │ 2. Remplir infos     │                 │                   │           │
│    │    (nom, email, rôle)│                 │                   │           │
│    │─────────────────────►│                 │                   │           │
│    │                      │                 │                   │           │
│    │ 3. Cliquer "Créer"   │                 │                   │           │
│    │─────────────────────►│                 │                   │           │
│    │                      │                 │                   │           │
│    │                      │ 4. Vérifier email│                  │           │
│    │                      │    unique       │                   │           │
│    │                      │─────────────────►│                  │           │
│    │                      │                 │                   │           │
│    │                      │                 │ 5. load_users()   │           │
│    │                      │                 │──────────────────►│           │
│    │                      │                 │                   │           │
│    │                      │                 │ 6. Vérifier       │           │
│    │                      │                 │    unicité        │           │
│    │                      │                 │◄──────────────────│           │
│    │                      │                 │                   │           │
│    │                      │ 7. Email OK     │                   │           │
│    │                      │◄────────────────│                   │           │
│    │                      │                 │                   │           │
│    │                      │ 8. Générer mdp  │                   │           │
│    │                      │    temporaire   │                   │           │
│    │                      │─────────────────►│                  │           │
│    │                      │                 │                   │           │
│    │                      │                 │ 9. Hash bcrypt    │           │
│    │                      │                 │                   │           │
│    │                      │                 │ 10. save_users()  │           │
│    │                      │                 │──────────────────►│           │
│    │                      │                 │                   │           │
│    │                      │ 11. Confirmation│                   │           │
│    │                      │◄────────────────│                   │           │
│    │                      │                 │                   │           │
│    │ 12. Afficher succès  │                 │                   │           │
│    │◄─────────────────────│                 │                   │           │
│    │                      │                 │                   │           │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Description** : Ce diagramme de séquence illustre la création d'un utilisateur :
1. L'administrateur accède au formulaire de création d'utilisateur
2. Il remplit les informations (nom, email, rôle)
3. Le système vérifie que l'email est unique
4. Génération d'un mot de passe temporaire
5. Hachage bcrypt du mot de passe
6. Sauvegarde dans le fichier JSON
7. Confirmation de création avec affichage des identifiants

Les validations incluent : unicité de l'email, format valide, rôle autorisé.

**Figure 3.6: Diagramme de séquence "Authentification" (Restauration de session)**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│           DIAGRAMME DE SÉQUENCE - AUTHENTIFICATION (SESSION)                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Utilisateur          Interface           Backend           Fichier JSON   │
│      │                    │                   │                   │         │
│      │ 1. Charger page    │                   │                   │         │
│      │───────────────────►│                   │                   │         │
│      │                    │                   │                   │         │
│      │                    │ 2. check_and_     │                   │         │
│      │                    │    restore_session│                   │         │
│      │                    │──────────────────►│                   │         │
│      │                    │                   │                   │         │
│      │                    │                   │ 3. Lire query     │         │
│      │                    │                   │    params         │         │
│      │                    │                   │                   │         │
│      │                    │                   │ 4. Vérifier token │         │
│      │                    │                   │    session        │         │
│      │                    │                   │                   │         │
│      │                    │                   │ 5. load_users()   │         │
│      │                    │                   │──────────────────►│         │
│      │                    │                   │                   │         │
│      │                    │                   │ 6. Vérifier user  │         │
│      │                    │                   │    actif          │         │
│      │                    │                   │◄──────────────────│         │
│      │                    │                   │                   │         │
│      │                    │ 7. Session OK     │                   │         │
│      │                    │◄──────────────────│                   │         │
│      │                    │                   │                   │         │
│      │                    │ 8. Restaurer      │                   │         │
│      │                    │    session_state  │                   │         │
│      │                    │                   │                   │         │
│      │ 9. Redirection     │                   │                   │         │
│      │    Dashboard       │                   │                   │         │
│      │◄───────────────────│                   │                   │         │
│      │                    │                   │                   │         │
│      │ [Alt: Session      │                   │                   │         │
│      │  invalide]         │                   │                   │         │
│      │◄───────────────────│                   │                   │         │
│      │ "Session expirée - │                   │                   │         │
│      │  Veuillez vous     │                   │                   │         │
│      │  reconnecter"      │                   │                   │         │
│      │                    │                   │                   │         │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Description** : Ce diagramme illustre la restauration automatique de session au chargement de la page :
1. L'utilisateur charge ou rafraîchit la page
2. L'interface appelle `check_and_restore_session()`
3. Le backend lit les query params pour récupérer le token de session
4. Vérification de la validité du token
5. Chargement des données utilisateurs depuis le fichier JSON
6. Vérification que le compte utilisateur est toujours actif
7. Si la session est valide, restauration du `session_state` (user_id, role, nom)
8. Redirection vers le tableau de bord avec les onglets adaptés au rôle
9. Si la session est invalide ou expirée, affichage du formulaire de connexion avec message

### 3.4.3 Diagramme de classe

**Figure 3.7: Diagramme de classe - Authentification/Gestion Utilisateurs**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              DIAGRAMME DE CLASSE - AUTHENTIFICATION & UTILISATEURS          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────┐         ┌─────────────────────┐                   │
│  │     Utilisateur     │         │       Session       │                   │
│  ├─────────────────────┤         ├─────────────────────┤                   │
│  │ - id: int           │         │ - user_id: int      │                   │
│  │ - nom: str          │         │ - username: str     │                   │
│  │ - email: str        │         │ - role: str         │                   │
│  │ - mot_de_passe: str │         │ - login_time: datetime│                 │
│  │ - role: Role        │◄────────│ - is_active: bool   │                   │
│  │ - actif: bool       │    1    │                     │                   │
│  │ - date_creation: date│        └─────────────────────┘                   │
│  ├─────────────────────┤                                                   │
│  │ + authentifier()    │                                                   │
│  │ + verifier_role()   │                                                   │
│  │ + desactiver()      │                                                   │
│  │ + reinitialiser_mdp()│                                                  │
│  └─────────────────────┘                                                   │
│           │                                                                 │
│           │ 1                                                             │
│           │                                                               │
│           ▼ *                                                              │
│  ┌─────────────────────┐                                                   │
│  │    Authentification │                                                   │
│  ├─────────────────────┤                                                   │
│  │ - email_input: str  │                                                   │
│  │ - password_input: str│                                                  │
│  │ - remember_me: bool │                                                   │
│  ├─────────────────────┤                                                   │
│  │ + login()           │                                                   │
│  │ + logout()          │                                                   │
│  │ + check_session()   │                                                   │
│  │ + restore_session() │                                                   │
│  │ + hash_password()   │                                                   │
│  │ + verify_password() │                                                   │
│  └─────────────────────┘                                                   │
│                                                                             │
│  ┌─────────────────────┐         ┌─────────────────────┐                   │
│  │   GestionUtilisateur│         │   Role (Enumération)│                   │
│  ├─────────────────────┤         ├─────────────────────┤                   │
│  │ - users_data: list  │         │ ADMIN = "admin"     │                   │
│  │ - current_user: User│         │ RECEPTION = "receptionniste"│             │
│  ├─────────────────────┤         │ MAINTENANCE = "maintenance"│              │
│  │ + creer_utilisateur()│        └─────────────────────┘                   │
│  │ + modifier_utilisateur()│                                                │
│  │ + supprimer_utilisateur()│                                               │
│  │ + lister_utilisateurs() │                                                │
│  │ + activer_compte()      │                                                │
│  │ + desactiver_compte()   │                                                │
│  └─────────────────────┘                                                   │
│                                                                             │
│  Relations:                                                                 │
│  ─────────                                                                  │
│  • Utilisateur "1" ──────► "*" Session (Un utilisateur peut avoir plusieurs│
│    sessions, mais une session appartient à un seul utilisateur)            │
│  • Utilisateur "1" ──────► "1" Authentification (Chaque tentative d'auth   │
│    est liée à un utilisateur)                                              │
│  • GestionUtilisateur ───► Utilisateur (Gère le CRUD des utilisateurs)     │
│  • Utilisateur ─────────► Role (Chaque utilisateur a un rôle défini)       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Description** : Ce diagramme de classe modélise le module d'authentification avec :
- **Utilisateur** : Classe principale avec attributs (id, nom, email, mot_de_passe, role, actif) et méthodes d'authentification
- **Session** : Gère la persistance de la connexion avec user_id, role, login_time
- **Authentification** : Classe utilitaire pour le login/logout, vérification de session, hachage bcrypt
- **GestionUtilisateur** : Classe administrative pour le CRUD des utilisateurs (création, modification, suppression, activation/désactivation)
- **Role** : Énumération des rôles possibles (admin, receptionniste, maintenance)

Les relations montrent la cardinalité entre les entités et l'héritage des fonctionnalités.

## 3.5 Réalisation

### 3.5.1 Interfaces d'Authentification

**Figure 3.10: Interface de connexion (Login)**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                      🏨 HOTEL MÉDITERRANÉE HAMMAMET                         │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │                         🔑 CONNEXION                                │   │
│  │                                                                     │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │  👤 Nom d'utilisateur                                       │   │   │
│  │  │  ┌─────────────────────────────────────────────────────┐    │   │   │
│  │  │  │                                                     │    │   │   │
│  │  │  └─────────────────────────────────────────────────────┘    │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  │                                                                     │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │  🔒 Mot de passe                                            │   │   │
│  │  │  ┌─────────────────────────────────────────────────────┐    │   │   │
│  │  │  │ ••••••••                                            │    │   │   │
│  │  │  └─────────────────────────────────────────────────────┘    │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  │                                                                     │   │
│  │  [✅] Se souvenir de moi (session 7 jours)                         │   │
│  │                                                                     │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │              🔑 SE CONNECTER                                  │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  │                                                                     │   │
│  │  ─────────────────── ou ───────────────────                         │   │
│  │                                                                     │   │
│  │  💡 Astuce: Cochez "Se souvenir de moi" pour rester                 │   │
│  │     connecté pendant 7 jours                                        │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Thème: Dark mode (fond #0f172a, accents #CC6D3D)                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Description** : L'interface de connexion présente un formulaire centré avec le logo et le nom de l'hôtel en en-tête. Les champs de saisie incluent le nom d'utilisateur et le mot de passe (masqué). Une case à cocher permet de persister la session pendant 7 jours via les query parameters. Le bouton de connexion utilise le thème sombre de l'application avec des accents orange (#CC6D3D). En cas d'erreur, un message d'erreur s'affiche sous le formulaire.

**Figure 3.11: Formulaire d'inscription (Création d'utilisateur)**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                    👤 GESTION DES UTILISATEURS                              │
│                                                                             │
│  ┌────────────────────────┐  ┌────────────────────────┐                    │
│  │  ADMINISTRATEURS       │  │  AUTRES UTILISATEURS   │                    │
│  │  ──────────────────    │  │  ─────────────────────   │                    │
│  │  • admin (Chef Maint.) │  │  • reception (Récép.)  │                    │
│  │                        │  │  • maintenance (Agent) │                    │
│  └────────────────────────┘  └────────────────────────┘                    │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  ➕ CRÉER UN NOUVEL UTILISATEUR                                     │   │
│  │                                                                     │   │
│  │  Nom d'utilisateur        [__________________]                    │   │
│  │  Nom complet              [__________________]                    │   │
│  │  Mot de passe             [__________________]                    │   │
│  │  Rôle                     [▼ receptionniste  ]                    │   │
│  │                           [▼ maintenance     ]                    │   │
│  │                                                                     │   │
│  │  [CRÉER L'UTILISATEUR]                                              │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  🗑️ SUPPRIMER UN UTILISATEUR                                        │   │
│  │                                                                     │   │
│  │  Sélectionner: [▼ maintenance ▼]  [🗑️ SUPPRIMER]                   │   │
│  │                                                                     │   │
│  │  ⚠️ Attention: Impossible de supprimer le compte admin ou           │   │
│  │     son propre compte                                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Description** : L'interface de gestion des utilisateurs est réservée à l'administrateur. Elle affiche la liste des utilisateurs existants classés par rôle (administrateurs vs autres). Le formulaire de création permet de définir le nom d'utilisateur, le nom complet, le mot de passe et le rôle (réceptionniste ou maintenance). La suppression est protégée par des validations empêchant la suppression du compte admin ou de son propre compte. Les modifications sont immédiatement persistées dans le fichier JSON.

### 3.5.2 Gestion des Utilisateurs

[Screenshots showing user management interface, listing existing users, edit/delete options, role management]

## 3.6 Conclusion

L'implémentation des fonctionnalités de connexion, d'inscription et de gestion des utilisateurs est 
achevée. Ces réalisations permettent de passer à l'étape suivante : la gestion des réservations et 
des chambres, constituant le cœur métier de l'application hôtelière.

---

# Chapitre 4 : Gestion des Réservations et Chambres

## 4.1 Introduction

Ce chapitre examine les fonctionnalités clés de gestion des réservations et des chambres, deux 
composantes essentielles de toute application hôtelière. Nous présentons d'abord le workflow dans 
notre tableau Kanban, suivi d'une analyse détaillée des processus de réservation et de gestion 
des chambres.

## 4.2 Tableau Kanban

**Figure 4.1: Tableau Kanban - Réservations et Chambres**

```
┌────────────────────────────────────────────────────────────────────────┐
│         TABLEAU KANBAN - RÉSERVATIONS & CHAMBRES                      │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  À TRAITER          │   EN COURS        │   EN TEST     │  COMPLÉTÉ  │
│  ─────────────────  │  ──────────────   │  ───────────  │  ────────  │
│  ┌─────────────┐   │  ┌─────────────┐  │  ┌─────────┐  │  ┌──────┐  │
│  │ Formulaire  │   │  │ Grid chambre│  │  │ Tests   │  │  │Liste │  │
│  │ réservation │   │  │ filtrable   │  │  │ conflits│  │  │chambres│ │
│  │ UI          │   │  │ par statut  │  │  │         │  │  │  OK  │  │
│  └─────────────┘   │  └─────────────┘  │  └─────────┘  │  └──────┘  │
│  ┌─────────────┐   │  ┌─────────────┐  │               │  ┌──────┐  │
│  │ Ajout       │   │  │ Mise à jour │  │               │  │Filtres│ │
│  │ chambre UI  │   │  │ statut      │  │               │  │aile/  │ │
│  │             │   │  │ chambre     │  │               │  │étage  │ │
│  └─────────────┘   │  └─────────────┘  │               │  └──────┘  │
│  ┌─────────────┐   │                   │               │            │
│  │ Historique  │   │                   │               │            │
│  │ maintenance │   │                   │               │            │
│  │ par chambre │   │                   │               │            │
│  └─────────────┘   │                   │               │            │
│                    │                   │               │            │
│  WIP Max: 5        │ WIP Max: 4        │ WIP Max: 2    │ Illimité   │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

**Description** : Ce tableau Kanban couvre le développement des fonctionnalités de réservation et de gestion des chambres :
- **À traiter** : Formulaire de création de réservation, ajout de chambre, historique de maintenance par chambre
- **En cours** : Grille des chambres filtrable, mise à jour du statut des chambres (Libre/Occupée/Maintenance)
- **En test** : Vérification des conflits de réservation et tests de disponibilité en temps réel
- **Complété** : Liste des chambres avec filtres par aile et étage opérationnelle

## 4.3 Backlog du produit

| Acteur | User Story | Complexité | Priorité |
|--------|------------|-----------|----------|
| Réceptionniste | En tant que réceptionniste, je peux consulter la disponibilité des chambres. | Moyenne | Forte |
| Réceptionniste | En tant que réceptionniste, je peux créer une nouvelle réservation. | Forte | Forte |
| Réceptionniste | En tant que réceptionniste, je peux modifier une réservation existante. | Forte | Forte |
| Réceptionniste | En tant que réceptionniste, je peux annuler une réservation. | Moyenne | Forte |
| Réceptionniste | En tant que réceptionniste, je peux enregistrer un nouveau client. | Moyenne | Moyenne |
| Administrateur | En tant qu'administrateur, je peux ajouter ou modifier une chambre. | Moyenne | Forte |
| Administrateur | En tant qu'administrateur, je peux gérer les catégories de chambres. | Moyenne | Moyenne |
| Gérant | En tant que gérant, je peux consulter les statistiques d'occupation des chambres. | Moyenne | Moyenne |

**Table 4.1: Backlog Gestion des Réservations et Chambres**

## 4.4 Les Diagrammes

### 4.4.1 Diagramme des cas d'utilisation

**Figure 4.2: Diagramme des cas d'utilisation "Réservations"**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CAS D'UTILISATION - RÉSERVATIONS                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Réceptionniste                                                           │
│       │                                                                     │
│       │ Créer réservation                                                    │
│       ├──────────────────────►┌─────────────────────────────┐              │
│       │                       │    Créer Réservation        │              │
│       │                       │    - Saisir client          │              │
│       │                       │    - Choisir chambre        │              │
│       │                       │    - Définir dates          │              │
│       │                       │    - Vérifier disponibilité │              │
│       │                       │    - Confirmer réservation  │              │
│       │                       └─────────────────────────────┘              │
│       │                                                                     │
│       │ Modifier réservation                                               │
│       ├──────────────────────►┌─────────────────────────────┐              │
│       │                       │   Modifier Réservation      │              │
│       │                       │   - Sélectionner réserv.    │              │
│       │                       │   - Changer dates/chambre   │              │
│       │                       │   - Recalculer montant      │              │
│       │                       │   - Confirmer modification  │              │
│       │                       └─────────────────────────────┘              │
│       │                                                                     │
│       │ Annuler réservation                                                │
│       ├──────────────────────►┌─────────────────────────────┐              │
│       │                       │   Annuler Réservation       │              │
│       │                       │   - Sélectionner réserv.    │              │
│       │                       │   - Motif d'annulation      │              │
│       │                       │   - Confirmer annulation    │              │
│       │                       │   - Notifier client         │              │
│       │                       └─────────────────────────────┘              │
│       │                                                                     │
│       │ Consulter disponibilité                                            │
│       ├──────────────────────►┌─────────────────────────────┐              │
│       │                       │   Consulter Disponibilité   │              │
│       │                       │   - Filtrer par date        │              │
│       │                       │   - Filtrer par type        │              │
│       │                       │   - Voir grille chambres    │              │
│       │                       │   - Détails chambre         │              │
│       │                       └─────────────────────────────┘              │
│       │                                                                     │
│   ┌───┴───┐                                                                 │
│   │ Système│                                                                 │
│   └───┬───┘                                                                 │
│       │ Vérifier conflits dates                                           │
│       │ Calculer montant séjour                                           │
│       │ Mettre à jour statut chambre                                      │
│       │ Enregistrer dans CSV                                              │
│       │                                                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Description** : Ce diagramme illustre les cas d'utilisation du module réservations, accessibles au réceptionniste :
- **Créer Réservation** : Le réceptionniste saisit les informations client, choisit une chambre, définit les dates de séjour. Le système vérifie la disponibilité en temps réel et calcule le montant total. Après confirmation, la chambre passe au statut "Réservée"
- **Modifier Réservation** : Permet de changer les dates, la chambre ou le client associé. Le système recalcule le montant et vérifie les nouveaux conflits éventuels
- **Annuler Réservation** : Annulation avec motif, mise à jour du statut de la chambre et notification automatique
- **Consulter Disponibilité** : Grille des chambres filtrable par date, type, aile et étage avec indicateurs visuels (Libre/Occupée/Maintenance)

Le système assure automatiquement la cohérence des données :
- Vérification des conflits de dates (pas de double-réservation)
- Calcul automatique du montant selon le tarif de la chambre et la durée
- Mise à jour en temps réel du statut des chambres

#### Raffinement du cas d'utilisation "Gérer Réservations"

| Cas d'utilisation | Gérer Réservations |
|------------------|--------|
| **Acteur** | Réceptionniste |
| **Pré-condition** | Réceptionniste authentifié, interface réservations accessible |
| **Post-condition** | Réservation créée/modifiée/annulée, statut chambre à jour |
| **Scénario nominal (Création)** | 1. Le réceptionniste accède au formulaire de création<br>2. Il saisit/selectionne le client<br>3. Il choisit la chambre et les dates<br>4. Le système vérifie la disponibilité<br>5. Le système calcule le montant<br>6. Le réceptionniste confirme<br>7. La réservation est enregistrée |
| **Scénario d'exception** | • Chambre non disponible → message erreur<br>• Dates invalides → validation échouée<br>• Client non trouvé → création rapide |

**Table 4.2: Raffinement du cas d'utilisation "Gérer Réservations"**

**Figure 4.3: Diagramme des cas d'utilisation "Gestion Chambres"**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CAS D'UTILISATION - GESTION DES CHAMBRES                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Administrateur                                                           │
│       │                                                                     │
│       │ Ajouter chambre                                                    │
│       ├──────────────────────►┌─────────────────────────────┐              │
│       │                       │    Ajouter Chambre          │              │
│       │                       │    - Saisir numéro          │              │
│       │                       │    - Choisir type           │              │
│       │                       │    - Définir aile/étage     │              │
│       │                       │    - Définir tarif          │              │
│       │                       │    - Confirmer ajout        │              │
│       │                       └─────────────────────────────┘              │
│       │                                                                     │
│       │ Modifier chambre                                                 │
│       ├──────────────────────►┌─────────────────────────────┐              │
│       │                       │   Modifier Chambre          │              │
│       │                       │   - Sélectionner chambre    │              │
│       │                       │   - Changer type/statut     │              │
│       │                       │   - Modifier tarif          │              │
│       │                       │   - Confirmer modification  │              │
│       │                       └─────────────────────────────┘              │
│       │                                                                     │
│       │ Gérer statut chambre                                             │
│       ├──────────────────────►┌─────────────────────────────┐              │
│       │                       │   Gérer Statut              │              │
│       │                       │   - Libre → Occupée         │              │
│       │                       │   - Occupée → Maintenance   │              │
│       │                       │   - Maintenance → Libre     │              │
│       │                       │   - Historique des changements             │
│       │                       └─────────────────────────────┘              │
│       │                                                                     │
│   Réceptionniste                                                           │
│       │                                                                     │
│       │ Consulter disponibilité                                          │
│       ├──────────────────────►┌─────────────────────────────┐              │
│       │                       │   Consulter Disponibilité   │              │
│       │                       │   - Voir grille chambres    │              │
│       │                       │   - Filtrer par statut      │              │
│       │                       │   - Détails par chambre     │              │
│       │                       └─────────────────────────────┘              │
│       │                                                                     │
│   Gérant                                                                   │
│       │                                                                     │
│       │ Voir statistiques occupation                                     │
│       ├──────────────────────►┌─────────────────────────────┐              │
│       │                       │   Statistiques Occupation   │              │
│       │                       │   - Taux d'occupation       │              │
│       │                       │   - Revenus par chambre     │              │
│       │                       │   - Performance par type    │              │
│       │                       └─────────────────────────────┘              │
│       │                                                                     │
│   ┌───┴───┐                                                                 │
│   │ Système│                                                                 │
│   └───┬───┘                                                                 │
│       │ Vérifier unicité numéro                                           │
│       │ Mettre à jour CSV chambres                                        │
│       │ Synchroniser avec réservations                                    │
│       │ Calculer statistiques temps réel                                  │
│       │                                                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Description** : Ce diagramme illustre les cas d'utilisation de gestion des chambres, accessibles selon les rôles :
- **Ajouter Chambre** (Admin) : Création d'une nouvelle chambre avec numéro, type (Standard/Deluxe/Suite), aile, étage et tarif
- **Modifier Chambre** (Admin) : Mise à jour des caractéristiques d'une chambre existante
- **Gérer Statut** (Admin/Réceptionniste) : Changement de statut (Libre → Occupée → Maintenance) avec historique des transitions
- **Consulter Disponibilité** (Réceptionniste) : Grille visuelle des chambres avec filtres par statut, type, aile et étage
- **Statistiques Occupation** (Gérant) : Indicateurs de performance (taux d'occupation, revenus, performance par catégorie)

Le système assure la synchronisation automatique entre le statut des chambres et les réservations actives.

#### Raffinement du cas d'utilisation "Gérer Chambres"

| Cas d'utilisation | Gérer Chambres |
|------------------|--------|
| **Acteur** | Administrateur / Réceptionniste |
| **Pré-condition** | Utilisateur authentifié avec les permissions appropriées |
| **Post-condition** | Chambre ajoutée/modifiée, statut mis à jour, données synchronisées |
| **Scénario nominal (Ajout)** | 1. L'administrateur accède au formulaire d'ajout<br>2. Il saisit le numéro de chambre<br>3. Il sélectionne le type et l'emplacement<br>4. Il définit le tarif de base<br>5. Le système vérifie l'unicité du numéro<br>6. La chambre est enregistrée dans le CSV |
| **Scénario d'exception** | • Numéro déjà existant → erreur<br>• Informations incomplètes → validation échouée<br>• Chambre en cours de réservation → modification limitée |

**Table 4.3: Raffinement du cas d'utilisation "Gérer Chambres"**

### 4.4.2 Diagramme de séquence

**Figure 4.4: Diagramme de séquence - Création d'une réservation**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│        DIAGRAMME DE SÉQUENCE - CRÉATION D'UNE RÉSERVATION                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Réceptionniste       Interface            Backend            Données      │
│       │                   │                    │                   │        │
│       │ 1. Accéder        │                    │                   │        │
│       │    formulaire     │                    │                   │        │
│       │──────────────────►│                    │                   │        │
│       │                   │                    │                   │        │
│       │ 2. Saisir client  │                    │                   │        │
│       │    (nom, email)   │                    │                   │        │
│       │──────────────────►│                    │                   │        │
│       │                   │                    │                   │        │
│       │ 3. Sélectionner   │                    │                   │        │
│       │    chambre        │                    │                   │        │
│       │──────────────────►│                    │                   │        │
│       │                   │                    │                   │        │
│       │ 4. Définir dates  │                    │                   │        │
│       │    (arrivée,      │                    │                   │        │
│       │    départ)        │                    │                   │        │
│       │──────────────────►│                    │                   │        │
│       │                   │                    │                   │        │
│       │ 5. Cliquer        │                    │                   │        │
│       │    "Vérifier       │                    │                   │        │
│       │    disponibilité" │                    │                   │        │
│       │──────────────────►│                    │                   │        │
│       │                   │                    │                   │        │
│       │                   │ 6. load_rooms()    │                   │        │
│       │                   │───────────────────►│                   │        │
│       │                   │                    │                   │        │
│       │                   │                    │ 7. Lire chambres  │        │
│       │                   │                    │   CSV             │        │
│       │                   │                    │──────────────────►│        │
│       │                   │                    │                   │        │
│       │                   │                    │ 8. Filtrer        │        │
│       │                   │                    │    chambres       │        │
│       │                   │                    │    disponibles    │        │
│       │                   │                    │◄──────────────────│        │
│       │                   │                    │                   │        │
│       │                   │ 9. Liste chambres  │                   │        │
│       │                   │    disponibles     │                   │        │
│       │                   │◄───────────────────│                   │        │
│       │                   │                    │                   │        │
│       │ 10. Afficher      │                    │                   │        │
│       │     grille        │                    │                   │        │
│       │◄──────────────────│                    │                   │        │
│       │                   │                    │                   │        │
│       │ 11. Confirmer     │                    │                   │        │
│       │     réservation   │                    │                   │        │
│       │──────────────────►│                    │                   │        │
│       │                   │                    │                   │        │
│       │                   │ 12. Vérifier       │                   │        │
│       │                   │     conflits       │                   │        │
│       │                   │     dates          │                   │        │
│       │                   │───────────────────►│                   │        │
│       │                   │                    │                   │        │
│       │                   │                    │ 13. Calculer      │        │
│       │                   │                    │     montant       │        │
│       │                   │                    │     (tarif × nuit)│        │
│       │                   │                    │                   │        │
│       │                   │                    │ 14. save_rooms()  │        │
│       │                   │                    │──────────────────►│        │
│       │                   │                    │                   │        │
│       │                   │ 15. Confirmation   │                   │        │
│       │                   │     création       │                   │        │
│       │                   │◄───────────────────│                   │        │
│       │                   │                    │                   │        │
│       │ 16. Afficher      │                    │                   │        │
│       │     succès +      │                    │                   │        │
│       │     numéro        │                    │                   │        │
│       │     réservation   │                    │                   │        │
│       │◄──────────────────│                    │                   │        │
│       │                   │                    │                   │        │
│       │ [Alt: Chambre     │                    │                   │        │
│       │  non dispo]       │                    │                   │        │
│       │◄──────────────────│                    │                   │        │
│       │ "Chambre indispo. │                    │                   │        │
│       │  Choisir dates    │                    │                   │        │
│       │  différentes"     │                    │                   │        │
│       │                   │                    │                   │        │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Description** : Ce diagramme de séquence illustre la création complète d'une réservation :
1. Le réceptionniste accède au formulaire de création de réservation
2. Saisie des informations client (nom, email, téléphone)
3. Sélection de la chambre souhaitée parmi la liste
4. Définition des dates d'arrivée et de départ
5. Demande de vérification de la disponibilité
6-9. Le backend charge les chambres depuis le CSV, filtre celles disponibles pour les dates sélectionnées et retourne la liste
10. Affichage de la grille des chambres disponibles avec leurs caractéristiques
11. Confirmation de la réservation par le réceptionniste
12-13. Le système vérifie les conflits de dates et calcule le montant total (tarif de la chambre × nombre de nuits)
14. Mise à jour du fichier CSV avec la nouvelle réservation
15-16. Confirmation de création avec affichage du numéro de réservation

**Flux alternatif** : Si la chambre n'est pas disponible aux dates choisies, un message d'erreur est affiché avec suggestion de dates alternatives.

**Figure 4.5: Diagramme de séquence - Gestion des chambres**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│        DIAGRAMME DE SÉQUENCE - GESTION DES CHAMBRES                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Admin/Réceptionniste  Interface          Backend           Données       │
│       │                    │                   │                   │        │
│       │ 1. Accéder         │                   │                   │        │
│       │    module          │                   │                   │        │
│       │    chambres        │                   │                   │        │
│       │───────────────────►│                   │                   │        │
│       │                    │                   │                   │        │
│       │                    │ 2. load_rooms()   │                   │        │
│       │                    │──────────────────►│                   │        │
│       │                    │                   │                   │        │
│       │                    │                   │ 3. Lire CSV       │        │
│       │                    │                   │    chambres       │        │
│       │                    │                   │──────────────────►│        │
│       │                    │                   │                   │        │
│       │                    │                   │ 4. Retourner      │        │
│       │                    │                   │    données        │        │
│       │                    │                   │◄──────────────────│        │
│       │                    │                   │                   │        │
│       │                    │ 5. Liste chambres │                   │        │
│       │                    │◄──────────────────│                   │        │
│       │                    │                   │                   │        │
│       │ 6. Afficher grille │                   │                   │        │
│       │    avec filtres    │                   │                   │        │
│       │◄───────────────────│                   │                   │        │
│       │                    │                   │                   │        │
│       │ [Alt 1: Ajouter    │                   │                   │        │
│       │  chambre]          │                   │                   │        │
│       │───────────────────►│                   │                   │        │
│       │ 7. Saisir infos    │                   │                   │        │
│       │    (num, type,     │                   │                   │        │
│       │    aile, étage)    │                   │                   │        │
│       │───────────────────►│                   │                   │        │
│       │                    │                   │                   │        │
│       │                    │ 8. Vérifier       │                   │        │
│       │                    │    unicité numéro │                   │        │
│       │                    │──────────────────►│                   │        │
│       │                    │                   │                   │        │
│       │                    │                   │ 9. Vérifier       │        │
│       │                    │                   │    dans CSV       │        │
│       │                    │                   │◄──────────────────│        │
│       │                    │                   │                   │        │
│       │                    │ 10. Numéro OK     │                   │        │
│       │                    │◄──────────────────│                   │        │
│       │                    │                   │                   │        │
│       │                    │ 11. save_rooms()  │                   │        │
│       │                    │──────────────────►│                   │        │
│       │                    │                   │                   │        │
│       │                    │                   │ 12. Enregistrer   │        │
│       │                    │                   │    dans CSV       │        │
│       │                    │                   │──────────────────►│        │
│       │                    │                   │                   │        │
│       │ 13. Confirmation   │                   │                   │        │
│       │     ajout          │                   │                   │        │
│       │◄───────────────────│                   │                   │        │
│       │                    │                   │                   │        │
│       │ [Alt 2: Modifier   │                   │                   │        │
│       │  statut]           │                   │                   │        │
│       │───────────────────►│                   │                   │        │
│       │ 14. Sélectionner   │                   │                   │        │
│       │     chambre +      │                   │                   │        │
│       │     nouveau statut │                   │                   │        │
│       │───────────────────►│                   │                   │        │
│       │                    │                   │                   │        │
│       │                    │ 15. update_room_  │                   │        │
│       │                    │     status()      │                   │        │
│       │                    │──────────────────►│                   │        │
│       │                    │                   │                   │        │
│       │                    │                   │ 16. Mettre à jour │        │
│       │                    │                   │     statut CSV    │        │
│       │                    │                   │──────────────────►│        │
│       │                    │                   │                   │        │
│       │ 17. Confirmation   │                   │                   │        │
│       │     mise à jour    │                   │                   │        │
│       │◄───────────────────│                   │                   │        │
│       │                    │                   │                   │        │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Description** : Ce diagramme de séquence illustre la gestion des chambres avec deux flux principaux :

**Flux principal** (Consultation) :
1. L'utilisateur accède au module de gestion des chambres
2-4. Le backend charge les données des chambres depuis le fichier CSV
5-6. Affichage de la grille des chambres avec les filtres disponibles (par aile, étage, type, statut)

**Flux alternatif 1** (Ajout d'une chambre) :
7. L'administrateur saisit les informations de la nouvelle chambre
8-10. Vérification de l'unicité du numéro de chambre
11-12. Enregistrement dans le fichier CSV
13. Confirmation de l'ajout

**Flux alternatif 2** (Modification du statut) :
14. L'utilisateur sélectionne une chambre et définit son nouveau statut (Libre/Occupée/Maintenance)
15-16. Mise à jour du statut dans le CSV
17. Confirmation de la mise à jour

Les statuts possibles sont : **Libre** (verte), **Occupée** (rouge), **Maintenance** (orange). La synchronisation avec les réservations est automatique.

### 4.4.3 Diagramme de classe

**Figure 4.6: Diagramme de classe - Réservations et Chambres**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│         DIAGRAMME DE CLASSE - RÉSERVATIONS & CHAMBRES                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────┐         ┌─────────────────────┐                   │
│  │      Réservation    │         │       Chambre       │                   │
│  ├─────────────────────┤         ├─────────────────────┤                   │
│  │ - id: int           │         │ - id: int           │                   │
│  │ - id_client: int    │         │ - numero_chambre: str│                  │
│  │ - id_chambre: int   │◄────────│ - type_chambre: str │                   │
│  │ - date_arrivee: date│   *     │ - aile: str         │                   │
│  │ - date_sortie: date │         │ - etage: int        │                   │
│  │ - heure_arrivee: str│         │ - status: str       │                   │
│  │ - heure_sortie: str │         │ - tarif: float      │                   │
│  │ - status: str       │         │ - capacite: int     │                   │
│  │ - remise: float     │         │ - description: str  │                   │
│  ├─────────────────────┤         ├─────────────────────┤                   │
│  │ + creer()           │         │ + changer_statut()  │                   │
│  │ + modifier()        │         │ + verifier_dispo()  │                   │
│  │ + annuler()         │         │ + get_historique()  │                   │
│  │ + calculer_montant()│         │ + mettre_a_jour()   │                   │
│  └─────────────────────┘         │ + ajouter()         │                   │
│           ▲                      └─────────────────────┘                   │
│           │                            ▲                                   │
│           │ *                          │ *                                  │
│           │                            │                                   │
│  ┌────────┴─────────┐        ┌─────────┴──────────┐                       │
│  │      Client      │        │   ComposantChambre │                       │
│  ├──────────────────┤        ├────────────────────┤                       │
│  │ - id: int        │        │ - id: int          │                       │
│  │ - nom_prenom: str│        │ - id_chambre: int  │                       │
│  │ - email: str     │        │ - nom_composant: str│                      │
│  │ - numero_telephone│       │ - date: date       │                       │
│  │ - type_client: str│       │ - description: str │                       │
│  │ - date_ajout: date│       │ - status: str      │                       │
│  ├──────────────────┤        ├────────────────────┤                       │
│  │ + ajouter()      │        │ + ajouter()        │                       │
│  │ + modifier()     │        │ + modifier_statut()│                       │
│  │ + supprimer()    │        │ + supprimer()      │                       │
│  │ + consulter()    │        │ + lister()         │                       │
│  └──────────────────┘        └────────────────────┘                       │
│                                                                             │
│  ┌─────────────────────┐                                                    │
│  │   TypePanne         │                                                    │
│  ├─────────────────────┤                                                    │
│  │ - nom_panne: str    │                                                    │
│  │ - priorite: str     │                                                    │
│  │ - description: str  │                                                    │
│  ├─────────────────────┤                                                    │
│  │ + lister()          │                                                    │
│  │ + ajouter()         │                                                    │
│  └─────────────────────┘                                                    │
│                                                                             │
│  Relations:                                                                 │
│  ─────────                                                                  │
│  • Réservation "*" ──────► "1" Chambre (Plusieurs réservations pour       │
│    une même chambre)                                                        │
│  • Réservation "*" ──────► "1" Client (Un client peut avoir plusieurs      │
│    réservations)                                                            │
│  • Chambre "1" ─────────► "*" ComposantChambre (Une chambre a plusieurs    │
│    composants)                                                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Description** : Ce diagramme de classe modélise la relation entre les réservations, les chambres et les clients :

- **Réservation** : Classe principale liant un client à une chambre pour une période donnée. Attributs clés : dates d'arrivée/sortie, heures, statut (Confirmée/Annulée/En attente), remise. Méthodes pour créer, modifier, annuler et calculer le montant total.
- **Chambre** : Représente l'inventaire des chambres avec numéro, type (Standard/Deluxe/Suite), aile, étage, statut (Libre/Occupée/Maintenance), tarif et capacité. Méthodes pour vérifier la disponibilité, changer le statut et consulter l'historique.
- **Client** : Informations client avec nom, email, téléphone, type de client. Méthodes CRUD classiques.
- **ComposantChambre** : Représente les équipements et composants d'une chambre (climatisation, TV, minibar, etc.) avec leur statut de fonctionnement. Utilisé pour le suivi de maintenance.
- **TypePanne** : Catalogue des types de pannes possibles avec niveau de priorité (Urgente/Normale/Faible).

Les cardinalités indiquent qu'une chambre peut avoir plusieurs réservations (successives) et qu'un client peut avoir plusieurs réservations. Une chambre est composée de plusieurs équipements (composants).

## 4.5 Réalisation

### 4.5.1 Interfaces de Gestion des Réservations

**Figure 4.7: Interface de gestion des réservations**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🏨 HOTEL MÉDITERRANÉE HAMMAMET          Tableau de Bord  Gérer Réservations│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  🛎️ GESTION DES RÉSERVATIONS                                         │   │
│  │                                                                     │   │
│  │  ┌──────────────────────────────────────────────────────────────┐  │   │
│  │  │  ➕ CRÉER UNE RÉSERVATION                                      │  │   │
│  │  │                                                              │  │   │
│  │  │  Type client: [▼ Nouveau client  ▼]                          │  │   │
│  │  │                                                              │  │   │
│  │  │  ╔════════════════════════════════════════════════════════╗  │  │   │
│  │  │  ║ Nom et Prénom          [__________________________]   ║  │  │   │
│  │  │  ║ Email                  [__________________________]   ║  │  │   │
│  │  │  ║ Numéro de téléphone    [__________________________]   ║  │  │   │
│  │  │  ╚════════════════════════════════════════════════════════╝  │  │   │
│  │  │                                                              │  │   │
│  │  │  Chambre: [▼ 01 - Standard - 120 DT / nuit ▼]              │  │   │
│  │  │                                                              │  │   │
│  │  │  Date d'arrivée:  [📅 25/04/2025]   Heure: [___14:00___]   │  │   │
│  │  │  Date de sortie :  [📅 27/04/2025]   Heure: [___12:00___]   │  │   │
│  │  │                                                              │  │   │
│  │  │  Remise: [__0__] %                                           │  │   │
│  │  │                                                              │  │   │
│  │  │  Montant total estimé: 240.0 DT                              │  │   │
│  │  │                                                              │  │   │
│  │  │  [🔄 VÉRIFIER DISPONIBILITÉ]    [💾 CRÉER LA RÉSERVATION]   │  │   │
│  │  └──────────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  📋 LISTE DES RÉSERVATIONS                                          │   │
│  │                                                                     │   │
│  │  Nbre de réservations: 3                                            │   │
│  │                                                                     │   │
│  │  ┌────┬──────────────┬────────┬──────────┬──────────┬────────┐     │   │
│  │  │ ID │ Nom Client   │Chambre │ Arrivée  │ Départ   │ Statut │     │   │
│  │  ├────┼──────────────┼────────┼──────────┼──────────┼────────┤     │   │
│  │  │ 1  │Ahmed Ben Ali │  101   │25/04/2025│27/04/2025│Confirmé│     │   │
│  │  │ 2  │Sarah Mansour │  102   │26/04/2025│29/04/2025│Confirmé│     │   │
│  │  │ 3  │Karim Zouari  │  103   │28/04/2025│30/04/2025│En att. │     │   │
│  │  └────┴──────────────┴────────┴──────────┴──────────┴────────┘     │   │
│  │                                                                     │   │
│  │  [✏️ Modifier] [🗑️ Annuler]                                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ⚠️ Remarque: Les réservations confirmées ne peuvent pas être modifiées    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Description** : L'interface de gestion des réservations est composée de deux sections principales :

**Section supérieure (Création)** :
- Sélection du type de client (nouveau ou existant)
- Formulaire de saisie des informations client avec champs obligatoires (nom, email, téléphone)
- Sélection de la chambre avec affichage du type et du tarif par nuit
- Sélection des dates d'arrivée et de départ avec heures de check-in/out
- Champ de remise (en pourcentage) avec calcul automatique du montant total
- Boutons d'action : Vérifier disponibilité (vérifie les conflits de dates) et Créer la réservation

**Section inférieure (Liste)** :
- Tableau récapitulatif de toutes les réservations avec ID, nom du client, chambre, dates et statut
- Actions disponibles : modifier ou annuler une réservation
- Les réservations confirmées sont protégées contre la modification
- Le nombre total de réservations est affiché en temps réel

### 4.5.2 Interfaces de Gestion des Chambres

**Figure 4.8: Interface de gestion des chambres**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🏨 HOTEL MÉDITERRANÉE HAMMAMET          Gérer Réservations  Gérer Chambres│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  🏨 GESTION DES CHAMBRES                                             │   │
│  │                                                                     │   │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │   │
│  │  │ 🟢 Chambres libres│  │ 🔴 Occupées     │  │ 🟠 Maintenance  │  │   │
│  │  │      15           │  │      8          │  │      2          │  │   │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘  │   │
│  │                                                                     │   │
│  │  Filtres:  Aile: [▼ Toutes ▼]  Étape: [▼ Tous ▼]  Statut: [▼ Tous ▼]│   │
│  │                                                                     │   │
│  │  ┌────┬────────┬──────────────┬──────────┬────────┬───────────┐    │   │
│  │  │ N° │ Type   │ Aile / Étage │ Statut   │ Tarif  │ Capacité  │    │   │
│  │  ├────┼────────┼──────────────┼──────────┼────────┼───────────┤    │   │
│  │  │ 101│Standard│ Aile A / RDC │ 🟢 Libre │120 DT  │ 2 pers.   │    │   │
│  │  │ 102│Deluxe  │ Aile A / RDC │ 🔴 Occupé│180 DT  │ 2 pers.   │    │   │
│  │  │ 103│Standard│ Aile A / 1er │ 🟢 Libre │120 DT  │ 2 pers.   │    │   │
│  │  │ 201│Suite   │ Aile B / 2ème│ 🟠 Maint.│350 DT  │ 4 pers.   │    │   │
│  │  │ 202│Standard│ Aile B / 2ème│ 🟢 Libre │120 DT  │ 2 pers.   │    │   │
│  │  └────┴────────┴──────────────┴──────────┴────────┴───────────┘    │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  ➕ AJOUTER UNE NOUVELLE CHAMBRE                                    │   │
│  │                                                                     │   │
│  │  Numéro: [____]  Type: [▼ Standard ▼]  Aile: [___]  Étage: [___]   │   │
│  │  Tarif: [____] DT  Capacité: [___] pers.                            │   │
│  │                                                                     │   │
│  │  [➕ AJOUTER LA CHAMBRE]                                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ⚠️ Les filtres permettent d'afficher uniquement les chambres correspondant│
│     aux critères sélectionnés                                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Description** : L'interface de gestion des chambres offre une vue synthétique et actionnable de l'inventaire :

**Indicateurs en temps réel** (cartes supérieures) :
- Chambres libres (vert) : 15
- Occupées (rouge) : 8
- En maintenance (orange) : 2

**Tableau des chambres** :
- Colonnes : Numéro, Type (Standard/Deluxe/Suite), Aile/Étage, Statut (avec code couleur), Tarif par nuit, Capacité
- Filtres combinables par aile, étage et statut pour une navigation efficace
- Les lignes sont triables par numéro, type ou tarif

**Formulaire d'ajout** :
- Champs : Numéro (unique), Type (liste déroulante), Aile, Étape, Tarif, Capacité
- Validation de l'unicité du numéro avant ajout
- Les nouvelles chambres sont immédiatement disponibles dans le tableau

Les couleurs de statut permettent une identification visuelle rapide : vert pour libre, rouge pour occupée, orange pour maintenance.

## 4.6 Conclusion

À l'issue de ce chapitre, les fonctionnalités essentielles de gestion des réservations et des chambres 
sont complètes. Ces éléments forment le cœur du système et permettent d'offrir une gestion opérationnelle 
cohérente de l'établissement hôtelier.

---

# Chapitre 5 : Gestion de la Maintenance et Tableau de Bord

## 5.1 Introduction

Ce chapitre aborde deux modules clés de l'application : la gestion de la maintenance et le tableau 
de bord analytique. Ces fonctionnalités permettent à l'établissement de gérer efficacement ses 
équipements et de disposer d'une vue d'ensemble de sa performance opérationnelle.

## 5.2 Tableau Kanban

**Figure 5.1: Tableau Kanban - Maintenance et Tableau de Bord**

## 5.3 Backlog du produit - Gestion de la Maintenance et Tableau de Bord

| Acteur | User Story | Complexité | Priorité |
|--------|------------|-----------|----------|
| Agent Entretien | En tant qu'agent d'entretien, je peux signaler une panne. | Moyenne | Forte |
| Agent Entretien | En tant qu'agent d'entretien, je peux consulter mes tâches assignées. | Moyenne | Forte |
| Agent Entretien | En tant qu'agent d'entretien, je peux mettre à jour l'état d'une tâche. | Moyenne | Forte |
| Administrateur | En tant qu'administrateur, je peux assigner des tâches aux agents. | Moyenne | Forte |
| Administrateur | En tant qu'administrateur, je peux consulter tous les rapports de maintenance. | Forte | Moyenne |
| Gérant | En tant que gérant, je peux visualiser le tableau de bord principal. | Moyenne | Forte |
| Gérant | En tant que gérant, je peux filtrer les données par date ou statut. | Moyenne | Moyenne |
| Gérant | En tant que gérant, je peux générer des rapports PDF. | Forte | Moyenne |

**Table 5.1: Backlog Gestion de la Maintenance et Tableau de Bord**

## 5.4 Les Diagrammes

### 5.4.1 Diagramme des cas d'utilisation

**Figure 5.2: Diagramme des cas d'utilisation "Gestion Maintenance"**
[Diagram showing Housekeeper reporting issues, updating status, and Maintenance coordination]

**Figure 5.3: Diagramme des cas d'utilisation "Tableau de Bord"**
[Diagram showing Manager viewing analytics, filtering data, and generating reports]

### 5.4.2 Diagramme de séquence

**Figure 5.4: Diagramme de séquence - Signalement de maintenance**
[Sequence diagram showing issue reporting and task assignment flow]

**Figure 5.5: Diagramme de séquence - Tableau de Bord**
[Sequence diagram showing dashboard data aggregation and visualization]

### 5.4.3 Diagramme de classe

**Figure 5.6: Diagramme de classe - Maintenance et Tableau de Bord**
[Class diagram showing Maintenance, MaintenanceTask, Pannes, Analytics classes]

## 5.5 Réalisation

### 5.5.1 Interface du Tableau de Bord

**Figure 5.7: Interface du tableau de bord principal**
[Screenshot showing: Occupancy rate, Revenue indicators, Pending tasks, Active pannes]

### 5.5.2 Interface de Gestion de la Maintenance

**Figure 5.8: Interface de gestion de la maintenance**
[Screenshot showing: Maintenance list, task assignment, status tracking, priority levels]

## 5.6 Conclusion

Avec l'achèvement de ce chapitre, tous les modules majeurs de l'application sont opérationnels. 
Le système offre une solution complète et intégrée de gestion hôtelière, couvrant les réservations, 
la gestion des chambres, la maintenance et l'analyse de performance.

---

# Conclusion Générale

Ce rapport représente le fruit d'un travail approfondi de conception et de développement d'une 
plateforme web intégrée de gestion hôtelière pour l'établissement Hôtel Méditerranée Nabeul, 
réalisé dans le cadre du projet de fin d'études pour l'obtention du diplôme d'Ingénieur en 
Business Intelligence à l'ITBS Nabeul.

Dans ce rapport, nous avons abordé plusieurs aspects essentiels de notre projet, allant de la 
planification et l'analyse à la réalisation et la validation de l'application.

## Résumé des chapitres

**Chapitre 1 : "Contexte du projet"** - Présente l'environnement de travail, le concept général 
et la méthodologie Kanban utilisée pour gérer les étapes du projet. Une étude de l'état de l'art 
a permis d'identifier les meilleures pratiques et technologies pour le développement d'une 
application web moderne.

**Chapitre 2 : "Analyse des Besoins"** - Détaille les exigences fonctionnelles et non fonctionnelles 
en collaboration avec les utilisateurs finaux. Nous avons défini l'architecture du système avec 
des diagrammes d'utilisation, de classe et un backlog de produit complet.

**Chapitre 3 : "Authentification/Gestion des Utilisateurs"** - Décrit la conception d'un système 
d'authentification sécurisé et la gestion des différents rôles d'utilisateurs. L'accent a été mis 
sur la sécurité, la performance et l'ergonomie de l'interface.

**Chapitre 4 : "Gestion des Réservations et Chambres"** - Couvre l'implémentation du cœur métier 
de l'application : la gestion des réservations, des clients et de l'inventaire des chambres. Les 
processus automatisés garantissent la cohérence des données et la prévention des double-bookings.

**Chapitre 5 : "Gestion de la Maintenance et Tableau de Bord"** - Décrit la création d'un système 
de suivi de maintenance performant et d'un tableau de bord analytique fournissant une vue 
d'ensemble complète de la performance de l'établissement.

## Compétences acquises

Ce projet m'a permis d'acquérir de nouvelles compétences techniques :
- Maîtrise de Streamlit pour le développement d'interfaces web rapides
- Expertise en Python et SQLAlchemy pour la gestion de bases de données
- Conception d'architectures logicielles robustes et scalables
- Implémentation de systèmes d'authentification sécurisés
- Développement de tableaux de bord analytiques interactifs
- Gestion de projet avec la méthodologie Kanban

J'ai également développé ma capacité d'analyse et de résolution de problèmes, renforcé ma 
compréhension des processus hôteliers et des enjeux de la gestion opérationnelle.

## Impact du projet

Cette plateforme offre à Hôtel Méditerranée :
- Une optimisation significative de ses processus opérationnels
- Une meilleure visibilité sur ses opérations en temps réel
- Une amélioration de la qualité du service client
- Une réduction des erreurs manuelles et des inefficacités
- Une base de données pour des décisions stratégiques fondées sur des données fiables
- La possibilité d'évoluer et d'adapter le système à de nouveaux besoins

## Perspectives futures

Des améliorations futures pourraient inclure :
- Intégration d'un système de paiement en ligne
- Application mobile pour accès sur smartphone/tablette
- Intégration avec les systèmes de gestion des revenus (RMS)
- Système de fidélisation des clients avancé
- Prévisions d'occupation basées sur le machine learning
- Intégration avec les plateformes de réservation online (Booking, Airbnb)

## Conclusion

Ce rapport de projet témoigne de mon engagement et de ma réussite dans la réalisation d'une 
solution concrète, moderne et utile pour le secteur hôtelier. La plateforme développée répond 
aux défis identifiés et offre une base solide pour l'optimisation continue des opérations 
d'Hôtel Méditerranée.

Je suis reconnaissant envers mon équipe de supervision, mes formateurs et tous ceux qui ont 
contribué à la réussite de ce projet. J'espère que ce travail pourra servir de référence et 
inspirer d'autres initiatives visant à moderniser et optimiser le secteur hôtelier tunisien 
et international.

---

# Webographie

1. Streamlit Official Documentation: https://docs.streamlit.io
2. Python Official Website: https://www.python.org
3. SQLAlchemy Documentation: https://docs.sqlalchemy.org
4. PostgreSQL Official Website: https://www.postgresql.org
5. Visual Studio Code: https://code.visualstudio.com
6. Plotly Official Documentation: https://plotly.com/python
7. Flask Official Website: https://flask.palletsprojects.com
8. Stack Overflow: https://stackoverflow.com
9. GitHub: https://github.com
10. Kanban Guide: https://www.kanbanize.com/kanban-resource/kanban-guide
11. Bootstrap Documentation: https://getbootstrap.com/docs
12. Redis Official Website: https://redis.io
13. Docker Official Website: https://www.docker.com
14. Postman Official Website: https://www.postman.com
15. Python Passlib Documentation: https://passlib.readthedocs.io
16. SQLAlchemy ORM Tutorial: https://docs.sqlalchemy.org/en/20/orm/index.html
17. IT Business School Nabeul: https://www.itbs-nabeul.tn
18. Hôtel Méditerranée Hammamet: https://hotel-mediterranee-hammamet.tn
19. Best Practices for Hotel Management Systems: https://www.hospitalitynet.org
20. RESTful API Design Guidelines: https://restfulapi.net

---

**Fin du Rapport de Projet de Fin d'Études**

*Diplôme National d'Ingénieur en Business Intelligence*  
*École Supérieure Privée des Technologies de l'Information et de Management de Nabeul*  
*Année Universitaire 2025-2026*
