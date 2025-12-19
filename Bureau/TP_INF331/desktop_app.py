# Lance le serveur Flask dans un thread séparé et ouvre une fenêtre de bureau avec PyQt5
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from threading import Thread

sys.path.insert(0, 'Backend')
from app import create_app

def run_flask():
    app = create_app()
    app.run(host='127.0.0.1', port=5002, debug=False)

if __name__ == '__main__':
    # Lancez le serveur Flask dans un thread
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Créez l'app de bureau
    qt_app = QApplication(sys.argv)
    view = QWebEngineView()
    view.load(QUrl('http://127.0.0.1:5002'))
    view.show()
    sys.exit(qt_app.exec_())
