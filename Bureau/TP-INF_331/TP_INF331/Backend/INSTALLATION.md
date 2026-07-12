# Guide d'Installation et Configuration - Marchés Locaux Backend

## 📋 Prérequis

- Python 3.8+
- pip (gestionnaire de paquets Python)
- Un IDE ou éditeur de texte (VSCode, PyCharm, etc.)

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/Tiomo-Ivan/MARCHES_LOCAUX.git
cd MARCHES_LOCAUX/Bureau/TP-INF_331/TP_INF331/Backend
```

### 2. Créer un environnement virtuel

```bash
# Sur Windows
python -m venv venv
venv\Scripts\activate

# Sur macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement

Créez un fichier `.env` à la racine du projet Backend :

```bash
# Développement
FLASK_ENV=development
FLASK_APP=run.py
SECRET_KEY=votre-clé-secrète-très-sécurisée

# Base de données
DATABASE_URL=sqlite:///marches_locaux.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Rate Limiting
RATELIMIT_STORAGE_URL=memory://
```

### 5. Démarrer l'application

```bash
python run.py
```

L'application sera accessible à `http://localhost:5000`

## 🔒 Améliorations de Sécurité Implémentées

### 1. **Protection CSRF**
- Tokens CSRF générés pour tous les formulaires
- Validation automatique des tokens dans les requêtes POST/PUT/DELETE
- Configuration selon l'environnement (HTTPS en production)

### 2. **Rate Limiting**
- Limite à 5 tentatives par heure pour les routes `/login` et `/register`
- Prévention des attaques par force brute
- Basé sur l'adresse IP du client

### 3. **Gestion des Mots de Passe**
- Hachage sécurisé avec PBKDF2-SHA256
- Validation de la force du mot de passe (minimum 8 caractères)
- Confirmation du mot de passe lors de l'inscription

### 4. **Validation des Données**
- Validation côté serveur de tous les champs d'entrée
- Validation du rôle (whitelist des rôles autorisés)
- Vérification des doublons (username, email)
- Gestion des erreurs robuste avec rollback DB

### 5. **Gestion des Sessions**
- Sessions sécurisées avec cookie HTTPOnly
- Timeout des sessions (7 jours par défaut)
- SameSite cookies pour prévenir les attaques CSRF

### 6. **Logging et Monitoring**
- Enregistrement de tous les événements d'authentification
- Logs d'erreur détaillés pour le débogage
- Gestion des erreurs HTTP (404, 500, 403)

## 📁 Structure du Projet

```
Backend/
├��─ app/
│   ├── __init__.py           # Initialisation Flask + CSRF
│   ├── blueprints/
│   │   ├── auth.py           # Routes d'authentification améliorées
│   │   ├── main.py
│   │   ├── markets.py
│   │   └── products.py
│   ├── models/               # Modèles SQLAlchemy
│   ├── utils/
│   │   └── validation_utils.py
│   ├── extensions.py         # Extensions Flask
│   └── events.py             # Événements SocketIO
├── config.py                 # Configuration (NOUVEAU)
├── requirements.txt          # Dépendances (NOUVEAU)
├── INSTALLATION.md           # Ce fichier
└── run.py                    # Point d'entrée
```

## 🧪 Tests

Pour tester les routes d'authentification :

```bash
# Installation des dépendances de test
pip install pytest pytest-flask

# Exécuter les tests
pytest tests/
```

## 🌍 Déploiement en Production

### Configuration Production

1. **Variables d'environnement essentielles** :
```bash
export FLASK_ENV=production
export SECRET_KEY=<une-clé-très-sécurisée>
export DATABASE_URL=postgresql://user:password@localhost/db_name
export RATELIMIT_STORAGE_URL=redis://localhost:6379
```

2. **Utiliser Gunicorn** :
```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

3. **Serveur Web (Nginx)** :
```nginx
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## ⚠️ Points Importants

1. **Changez le SECRET_KEY en production** - Utilisez une clé très sécurisée
2. **Utilisez HTTPS en production** - Assurez un certificat SSL valide
3. **Configurez une vraie base de données** - PostgreSQL ou MySQL en production
4. **Utilisez Redis pour le Rate Limiting** - Au lieu de memory:// en production
5. **Sauvegardez vos logs** - Archivez les logs régulièrement

## 📚 Ressources Utiles

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-WTF (CSRF Protection)](https://flask-wtf.readthedocs.io/)
- [Flask-Limiter (Rate Limiting)](https://flask-limiter.readthedocs.io/)
- [OWASP Security Guidelines](https://owasp.org/www-project-top-ten/)

## 🤝 Support

Pour toute question ou problème, contactez l'équipe de développement.
