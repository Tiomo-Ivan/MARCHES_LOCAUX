"""
Utilitaires pour la gestion des fichiers uploadés.

Fournit des fonctions pour valider et sauvegarder les fichiers image.
"""

import os
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """
    Vérifie si l'extension du fichier est autorisée.

    Args:
        filename (str): Nom du fichier.

    Returns:
        bool: True si l'extension est autorisée.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, subfolder='products'):
    """
    Sauvegarde un fichier uploadé dans le dossier approprié.

    Args:
        file: Objet fichier de Flask.
        subfolder (str): Sous-dossier dans static/images/.

    Returns:
        str or None: Nom du fichier sauvegardé, ou None si invalide.
    """
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(current_app.root_path, '..', '..', 'Frontend', 'static', 'images', subfolder)
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return filename
    return None