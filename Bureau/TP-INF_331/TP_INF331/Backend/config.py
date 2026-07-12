# Configuration - Marchés Locaux Backend

import os
from datetime import timedelta

class Config:
    """
    Configuration de base pour l'application Flask.
    
    Cette classe contient les paramètres de configuration communs
    à tous les environnements.
    """
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Base de données
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///marches_locaux.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CSRF Protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_CHECK_DEFAULT = True
    WTF_CSRF_SSL_STRICT = False  # À mettre à True en production avec HTTPS
    WTF_CSRF_TIME_LIMIT = None  # Pas de limite de temps pour les tokens CSRF
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL') or 'memory://'
    RATELIMIT_ENABLED = True
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = os.environ.get('LOG_FILE') or 'logs/app.log'
    
    # SocketIO
    SOCKETIO_ASYNC_MODE = 'threading'
    SOCKETIO_CORS_ALLOWED_ORIGINS = os.environ.get('SOCKETIO_CORS_ALLOWED_ORIGINS', '*')
    
    # Validation
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file upload
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    """
    Configuration pour l'environnement de développement.
    """
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False  # Pour le développement en HTTP
    WTF_CSRF_SSL_STRICT = False


class ProductionConfig(Config):
    """
    Configuration pour l'environnement de production.
    """
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True  # Require HTTPS
    WTF_CSRF_SSL_STRICT = True  # Enforce HTTPS for CSRF
    
    # Base de données production (doit être définie via variable d'environnement)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL environment variable not set in production!")


class TestingConfig(Config):
    """
    Configuration pour les tests.
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False  # Désactiver CSRF pour les tests
    RATELIMIT_ENABLED = False  # Désactiver rate limiting pour les tests


# Sélectionner la configuration en fonction de l'environnement
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
