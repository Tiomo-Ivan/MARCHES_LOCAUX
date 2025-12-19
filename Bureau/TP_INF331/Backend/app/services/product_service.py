"""
Services métier pour la gestion des produits.

Contient les fonctions de création et mise à jour des produits,
avec gestion des fichiers image.
"""

import logging
from ..extensions import db
from ..models import Product
from ..utils.file_utils import save_uploaded_file

logger = logging.getLogger(__name__)

def create_product(name, description, price, quantity, market_id, seller_id, image_file=None):
    """
    Crée un nouveau produit.

    Args:
        name (str): Nom du produit.
        description (str): Description du produit.
        price (float): Prix du produit.
        quantity (int): Quantité disponible.
        market_id (int): ID du marché.
        seller_id (int): ID du vendeur.
        image_file: Fichier image uploadé (optionnel).

    Returns:
        Product: L'instance du produit créé.
    """
    # Gestion de l'upload d'image si fournie
    image = None
    if image_file:
        image = save_uploaded_file(image_file)
    product = Product(
        name=name,
        description=description,
        price=price,
        quantity=quantity,
        image=image,
        market_id=market_id,
        seller_id=seller_id
    )
    db.session.add(product)
    db.session.commit()
    logger.info(f"Produit créé: {name} (vendeur ID: {seller_id})")
    return product

def update_product(product, name, description, price, quantity, market_id, image_file=None):
    """
    Met à jour un produit existant.

    Args:
        product (Product): Instance du produit à modifier.
        name (str): Nouveau nom.
        description (str): Nouvelle description.
        price (float): Nouveau prix.
        quantity (int): Nouvelle quantité.
        market_id (int): Nouvel ID de marché.
        image_file: Nouveau fichier image (optionnel).
    """
    product.name = name
    product.description = description
    product.price = price
    product.quantity = quantity
    product.market_id = market_id
    if image_file:
        image = save_uploaded_file(image_file)
        if image:
            product.image = image
    db.session.commit()
    logger.info(f"Produit mis à jour: {product.name} (ID: {product.id})")
    return product