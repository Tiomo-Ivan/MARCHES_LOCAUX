"""
Point d'entrée principal de l'application.

Crée l'application Flask et lance le serveur avec SocketIO.
"""

import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

from app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    socketio.run(app, debug=debug, port=port)
