"""
Initialisation de l'application Flask.

Ce module configure l'application Flask principale, initialise les extensions
comme SQLAlchemy et SocketIO, et enregistre les blueprints pour les différentes
fonctionnalités de l'application.
"""

import logging
import os
from flask import Flask
from flask_socketio import SocketIO
from .extensions import db
from .events import init_socketio_events
from .blueprints.main import main
from .blueprints.auth import auth
from .blueprints.markets import markets
from .blueprints.products import products

socketio = SocketIO(cors_allowed_origins="*")  # Autorise les connexions depuis n'importe quelle origine (à ajuster en production)

def create_app():
    """
    Crée et configure l'application Flask.

    Initialise Flask avec les dossiers de templates et statiques,
    charge la configuration, initialise les extensions et enregistre
    les blueprints. Crée également les tables de base de données.
    Configure le système de logging.

    Returns:
        Flask: L'application Flask configurée.
    """
    app = Flask(__name__, template_folder='../../Frontend/templates', static_folder='../../Frontend/static')
    app.config.from_object('config.Config')

    # Configuration du logging
    log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO').upper())
    log_file = app.config.get('LOG_FILE', 'app.log')

    # Créer le dossier logs si nécessaire
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    app.logger.info("Application Flask démarrée")

    db.init_app(app)
    socketio.init_app(app)
    init_socketio_events(socketio)

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(markets)
    app.register_blueprint(products)

    with app.app_context():
        db.create_all()
        app.logger.info("Tables de base de données créées")

    # Gestionnaires d'erreurs
    @app.errorhandler(404)
    def page_not_found(e):
        app.logger.warning(f"Page 404 demandée: {request.url}")
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(e):
        app.logger.error(f"Erreur 500: {str(e)}")
        db.session.rollback()  # Rollback en cas d'erreur DB
        return render_template('500.html'), 500

    @app.errorhandler(403)
    def forbidden(e):
        app.logger.warning(f"Accès interdit: {request.url}")
        flash("Vous n'avez pas les permissions nécessaires.", "danger")
        return redirect(url_for('main.index'))

    return app
