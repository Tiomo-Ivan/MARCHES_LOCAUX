"""
Utilitaires de validation pour les données utilisateur.
"""

import re
from flask import flash


def validate_username(username):
    """
    Valide un nom d'utilisateur.

    Args:
        username (str): Nom d'utilisateur à valider.

    Returns:
        bool: True si valide.
    """
    if not username or len(username) < 3:
        flash("Le nom d'utilisateur doit contenir au moins 3 caractères.", "danger")
        return False
    if len(username) > 50:
        flash("Le nom d'utilisateur ne peut pas dépasser 50 caractères.", "danger")
        return False
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        flash("Le nom d'utilisateur ne peut contenir que des lettres, chiffres et underscores.", "danger")
        return False
    return True


def validate_email(email):
    """
    Valide une adresse email.

    Args:
        email (str): Email à valider.

    Returns:
        bool: True si valide.
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not email or not re.match(email_pattern, email):
        flash("Veuillez entrer une adresse email valide.", "danger")
        return False
    if len(email) > 100:
        flash("L'adresse email ne peut pas dépasser 100 caractères.", "danger")
        return False
    return True


def validate_password(password):
    """
    Valide un mot de passe.

    Args:
        password (str): Mot de passe à valider.

    Returns:
        bool: True si valide.
    """
    if not password or len(password) < 6:
        flash("Le mot de passe doit contenir au moins 6 caractères.", "danger")
        return False
    return True


def validate_product_name(name):
    """
    Valide le nom d'un produit.

    Args:
        name (str): Nom du produit.

    Returns:
        bool: True si valide.
    """
    if not name or len(name.strip()) < 2:
        flash("Le nom du produit doit contenir au moins 2 caractères.", "danger")
        return False
    if len(name) > 100:
        flash("Le nom du produit ne peut pas dépasser 100 caractères.", "danger")
        return False
    return True


def validate_product_price(price_str):
    """
    Valide et convertit le prix d'un produit.

    Args:
        price_str (str): Prix en string.

    Returns:
        float or None: Prix validé ou None si invalide.
    """
    try:
        price = float(price_str)
        if price <= 0:
            flash("Le prix doit être supérieur à 0.", "danger")
            return None
        if price > 1000000:  # Limite arbitraire
            flash("Le prix semble trop élevé.", "danger")
            return None
        return price
    except ValueError:
        flash("Veuillez entrer un prix valide.", "danger")
        return None


def validate_product_quantity(quantity_str):
    """
    Valide et convertit la quantité d'un produit.

    Args:
        quantity_str (str): Quantité en string.

    Returns:
        int or None: Quantité validée ou None si invalide.
    """
    if not quantity_str:
        return None  # Quantité optionnelle
    try:
        quantity = int(quantity_str)
        if quantity < 0:
            flash("La quantité ne peut pas être négative.", "danger")
            return None
        if quantity > 10000:  # Limite arbitraire
            flash("La quantité semble trop élevée.", "danger")
            return None
        return quantity
    except ValueError:
        flash("Veuillez entrer une quantité valide.", "danger")
        return None