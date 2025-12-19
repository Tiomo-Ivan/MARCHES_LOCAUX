# Marchés Locaux - Application Web Flask

## Description du Projet

Cette application web développée avec Flask permet de connecter les vendeurs locaux et les acheteurs dans les marchés de Yaoundé. Elle facilite la mise en relation entre producteurs et consommateurs en offrant une plateforme moderne pour la commercialisation des produits locaux.

Le projet a été réalisé dans le cadre d'un travail pratique universitaire pour illustrer les concepts de développement web avec Flask, gestion de base de données SQLAlchemy, et architecture d'application web.

## Fonctionnalités Principales

### Pour les Acheteurs
- Consultation du catalogue des produits disponibles
- Recherche et filtrage par marché, nom de produit, prix
- Visualisation détaillée des produits avec images
- Chat en temps réel avec les vendeurs
- Géolocalisation des marchés avec cartes interactives

### Pour les Vendeurs
- Gestion de leur catalogue de produits
- Ajout/modification/suppression de produits avec upload d'images
- Gestion des messages avec les acheteurs
- Accès à leur tableau de bord personnel

### Pour les Administrateurs
- Gestion complète des marchés (CRUD)
- Supervision des utilisateurs et produits
- Maintenance de la plateforme

## Structure du Projet

```
TP_INF331/
├── Backend/                    # Code Python de l'application
│   ├── app/                   # Package principal
│   │   ├── blueprints/        # Routes organisées par fonctionnalités
│   │   ├── models/           # Modèles de données SQLAlchemy
│   │   ├── services/         # Logique métier
│   │   ├── utils/            # Utilitaires et helpers
│   │   ├── __init__.py       # Initialisation Flask
│   │   ├── events.py         # Gestion SocketIO
│   │   └── extensions.py     # Extensions Flask
│   ├── config.py             # Configuration
│   ├── requirements.txt      # Dépendances Python
│   ├── run.py               # Point d'entrée
│   └── seed_markets.py      # Script d'initialisation DB
├── Frontend/                 # Templates et assets statiques
│   ├── static/
│   │   ├── css/             # Feuilles de style organisées
│   │   ├── images/          # Images uploadées
│   │   └── js/              # JavaScript
│   └── templates/           # Templates Jinja2
├── .gitignore               # Fichiers à ignorer
└── README.md               # Documentation
```

## Installation et Exécution

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'Installation

1. **Cloner le projet**
   ```bash
   git clone <url-du-projet>
   cd TP_INF331
   ```

2. **Créer l'environnement virtuel**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

3. **Configurer les variables d'environnement**
   ```bash
   cp .env.example .env
   # Éditez .env selon vos besoins (clé secrète, port, etc.)
   ```

4. **Installer les dépendances**
   ```bash
   pip install -r Backend/requirements.txt
   ```

5. **Initialiser la base de données**
   ```bash
   cd Backend
   python -c "from app import create_app; app = create_app()"
   python seed_markets.py
   ```

6. **Lancer les tests (optionnel)**
   ```bash
   cd Backend
   pytest
   ```

7. **Lancer l'application**
   ```bash
   python run.py
   ```

L'application sera accessible sur `http://localhost:5002`

## Choix Techniques

### Framework et Librairies
- **Flask** : Framework web léger et flexible
- **Flask-SQLAlchemy** : ORM pour l'interaction avec la base de données SQLite
- **Flask-SocketIO** : Gestion du temps réel pour le chat
- **Bootstrap 5** : Framework CSS pour l'interface utilisateur
- **Leaflet** : Cartes interactives pour la géolocalisation

### Architecture
- **Pattern Blueprint** : Organisation modulaire des routes
- **Séparation MVC** : Modèles, vues (templates), contrôleurs (routes)
- **Services** : Extraction de la logique métier des contrôleurs
- **Utilitaires** : Fonctions helpers réutilisables

### Base de Données
- **SQLite** : Base de données fichier adaptée au développement
- **Modèle relationnel** : Utilisateurs, Produits, Marchés, Messages
- **Contraintes d'intégrité** : Clés étrangères et suppression en cascade

### Sécurité
- **Gestion des sessions** : Authentification utilisateur
- **Validation des formulaires** : Côté serveur
- **Protection CSRF** : Via les secrets Flask
- **Upload sécurisé** : Validation des extensions de fichiers

## Limites et Améliorations Possibles

### Limites Actuelles
- Base de données SQLite (non adaptée à la production)
- Pas de tests automatisés
- Interface limitée aux marchés de Yaoundé
- Gestion basique des images (pas d'optimisation)

### Améliorations Possibles
- Migration vers PostgreSQL pour la production
- Ajout de tests unitaires et d'intégration
- Système de notifications push
- API REST pour intégrations tierces
- Optimisation des images (redimensionnement, compression)
- Système de paiement intégré
- Application mobile complémentaire
- Internationalisation (i18n)


---
