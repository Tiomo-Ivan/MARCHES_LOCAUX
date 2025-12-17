"""
Modèles de données pour les produits.

Définit le modèle Product avec ses attributs et relations.
"""

from ..extensions import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    image = db.Column(db.String(100), nullable=True)
    market_id = db.Column(db.Integer, db.ForeignKey('market.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    seller = db.relationship('User', backref='products')