"""
Tests basiques pour les routes de l'application Marchés Locaux.
"""

import pytest
from app import create_app
from app.models import User, Market, Product
from app.extensions import db


@pytest.fixture
def app():
    """Fixture pour créer l'application de test."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        # Créer des données de test
        market = Market(name="Marché Test", city="Test", latitude=0.0, longitude=0.0)
        db.session.add(market)
        db.session.commit()
        yield app


@pytest.fixture
def client(app):
    """Fixture pour le client de test."""
    return app.test_client()


def test_home_page(client):
    """Test d'accès à la page d'accueil."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'MARCHES LOCAUX' in response.data


def test_products_page_redirect_seller(client, app):
    """Test de redirection des vendeurs vers leur catalogue."""
    with app.app_context():
        # Créer un vendeur de test
        user = User(username="vendeur_test", email="vendeur@test.com",
                   password_hash="hash", role="seller")
        db.session.add(user)
        db.session.commit()

        with client.session_transaction() as sess:
            sess['user_id'] = user.id
            sess['user_role'] = user.role

        response = client.get('/products')
        assert response.status_code == 302  # Redirection
        assert '/my-products' in response.headers['Location']


def test_login_page(client):
    """Test d'accès à la page de connexion."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Connexion' in response.data


def test_register_page(client):
    """Test d'accès à la page d'inscription."""
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Inscription' in response.data


def test_products_list_without_auth(client):
    """Test d'accès à la liste des produits sans authentification."""
    response = client.get('/products')
    assert response.status_code == 200


def test_markets_list(client):
    """Test d'accès à la liste des marchés."""
    response = client.get('/markets')
    assert response.status_code == 200


def test_invalid_route(client):
    """Test d'une route inexistante."""
    response = client.get('/route-inexistante')
    assert response.status_code == 404