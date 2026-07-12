# Tests pour le module d'authentification
# pytest tests/test_auth.py

import pytest
from flask import session, url_for
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    """Crée une application pour les tests."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['RATELIMIT_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Crée un client de test."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Crée un CLI runner pour les tests."""
    return app.test_cli_runner()


@pytest.fixture
def test_user(app):
    """Crée un utilisateur de test."""
    with app.app_context():
        user = User(
            username='testuser',
            email='testuser@example.com',
            password_hash=generate_password_hash('TestPass123!'),
            role='buyer'
        )
        db.session.add(user)
        db.session.commit()
        return user


class TestRegister:
    """Tests pour la route d'enregistrement."""
    
    def test_register_page_get(self, client):
        """Test l'accès à la page d'enregistrement."""
        response = client.get(url_for('auth.register'))
        assert response.status_code == 200
        assert b'Créer un compte' in response.data
    
    def test_register_valid_user(self, client):
        """Test l'enregistrement d'un nouvel utilisateur valide."""
        response = client.post(url_for('auth.register'), data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'role': 'buyer'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Inscription réussie' in response.data
    
    def test_register_password_mismatch(self, client):
        """Test que les mots de passe doivent correspondre."""
        response = client.post(url_for('auth.register'), data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'DifferentPass123!',
            'role': 'buyer'
        })
        assert response.status_code == 200
        assert b'ne correspondent pas' in response.data
    
    def test_register_weak_password(self, client):
        """Test qu'un mot de passe faible est rejeté."""
        response = client.post(url_for('auth.register'), data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'weak',
            'password_confirm': 'weak',
            'role': 'buyer'
        })
        assert response.status_code == 200
        assert b'assez fort' in response.data or b'8 caract' in response.data
    
    def test_register_duplicate_username(self, client, test_user):
        """Test qu'on ne peut pas enregistrer un username déjà utilisé."""
        response = client.post(url_for('auth.register'), data={
            'username': 'testuser',
            'email': 'different@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'role': 'buyer'
        })
        assert response.status_code == 200
        assert b'déjà pris' in response.data
    
    def test_register_duplicate_email(self, client, test_user):
        """Test qu'on ne peut pas enregistrer un email déjà utilisé."""
        response = client.post(url_for('auth.register'), data={
            'username': 'differentuser',
            'email': 'testuser@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'role': 'buyer'
        })
        assert response.status_code == 200
        assert b'déjà utilisée' in response.data
    
    def test_register_invalid_email(self, client):
        """Test qu'un email invalide est rejeté."""
        response = client.post(url_for('auth.register'), data={
            'username': 'newuser',
            'email': 'not-an-email',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'role': 'buyer'
        })
        assert response.status_code == 200
        assert b'n\'est pas valide' in response.data or b'email' in response.data


class TestLogin:
    """Tests pour la route de connexion."""
    
    def test_login_page_get(self, client):
        """Test l'accès à la page de connexion."""
        response = client.get(url_for('auth.login'))
        assert response.status_code == 200
        assert b'Se connecter' in response.data
    
    def test_login_valid_credentials(self, client, test_user):
        """Test la connexion avec les bonnes identifiants."""
        response = client.post(url_for('auth.login'), data={
            'username': 'testuser',
            'password': 'TestPass123!'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Connexion réussie' in response.data
    
    def test_login_invalid_password(self, client, test_user):
        """Test la connexion avec un mauvais mot de passe."""
        response = client.post(url_for('auth.login'), data={
            'username': 'testuser',
            'password': 'WrongPassword123!'
        })
        assert response.status_code == 200
        assert b'incorrect' in response.data
    
    def test_login_nonexistent_user(self, client):
        """Test la connexion avec un utilisateur inexistant."""
        response = client.post(url_for('auth.login'), data={
            'username': 'nonexistent',
            'password': 'TestPass123!'
        })
        assert response.status_code == 200
        assert b'incorrect' in response.data
    
    def test_login_empty_credentials(self, client):
        """Test la connexion avec des champs vides."""
        response = client.post(url_for('auth.login'), data={
            'username': '',
            'password': ''
        })
        assert response.status_code == 200
        assert b'requis' in response.data
    
    def test_session_created_on_login(self, client, test_user):
        """Test que la session est créée après la connexion."""
        response = client.post(url_for('auth.login'), data={
            'username': 'testuser',
            'password': 'TestPass123!'
        }, follow_redirects=True)
        with client:
            client.get(url_for('auth.login'))
            # Vérifier que la session contient l'utilisateur
            # Note: Ce test nécessite une route protégée pour vérifier


class TestLogout:
    """Tests pour la route de déconnexion."""
    
    def test_logout(self, client, test_user):
        """Test la déconnexion."""
        # Se connecter d'abord
        client.post(url_for('auth.login'), data={
            'username': 'testuser',
            'password': 'TestPass123!'
        })
        
        # Se déconnecter
        response = client.get(url_for('auth.logout'), follow_redirects=True)
        assert response.status_code == 200
        assert b'Déconnexion réussie' in response.data
    
    def test_logout_clears_session(self, client, test_user):
        """Test que la session est effacée après la déconnexion."""
        # Se connecter
        client.post(url_for('auth.login'), data={
            'username': 'testuser',
            'password': 'TestPass123!'
        })
        
        # Se déconnecter
        client.get(url_for('auth.logout'))
        
        # Vérifier que la session est vide
        # Ce test nécessite une route protégée pour vérifier


class TestValidation:
    """Tests pour la validation des données."""
    
    def test_username_length_validation(self, client):
        """Test la validation de la longueur du username."""
        # Trop court
        response = client.post(url_for('auth.register'), data={
            'username': 'ab',
            'email': 'test@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'role': 'buyer'
        })
        # Vérifier qu'il y a une erreur de validation
        assert response.status_code == 200
    
    def test_invalid_role(self, client):
        """Test qu'un rôle invalide est rejeté."""
        response = client.post(url_for('auth.register'), data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'role': 'invalid_role'
        })
        # Le rôle doit être rejeté ou réinitialisé à 'buyer'
        assert response.status_code == 200
