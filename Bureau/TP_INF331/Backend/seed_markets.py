#!/usr/bin/env python3
"""
Script d'initialisation de la base de données avec les marchés de Yaoundé.

Insère 10 marchés avec leurs coordonnées GPS s'ils n'existent pas déjà.
Le script est idempotent et peut être exécuté plusieurs fois sans créer de doublons.
"""

from app import create_app
from app.models import Market
from app.extensions import db

# Data for the 10 markets in Yaoundé
MARKETS_DATA = [
    {"name": "Marché Etoudi", "latitude": 3.9155625, "longitude": 11.5292031},
    {"name": "Marché Nsam", "latitude": 3.8291875, "longitude": 11.5089844},
    {"name": "Marché Mendong", "latitude": 3.8360625, "longitude": 11.4708125},
    {"name": "Marché Biyem-Assi", "latitude": 3.8418125, "longitude": 11.4887656},
    {"name": "Marché Nkolbisson", "latitude": 3.8726875, "longitude": 11.4543125},
    {"name": "Marché Essos", "latitude": 3.8696125, "longitude": 11.5436094},
    {"name": "Marché Melen", "latitude": 3.8663625, "longitude": 11.4865469},
    {"name": "Marché Mfoundi", "latitude": 3.8657625, "longitude": 11.5231406},
    {"name": "Marché Mokolo", "latitude": 3.8736125, "longitude": 11.5010781},
    {"name": "Marché Central", "latitude": 3.8640375, "longitude": 11.5190781},
]

def seed_markets():
    """Seed the database with market data."""
    app = create_app()
    with app.app_context():
        print("Starting market seeding process...")

        created_count = 0
        existing_count = 0

        for market_data in MARKETS_DATA:
            # Check if market already exists
            existing_market = Market.query.filter_by(name=market_data["name"]).first()

            if existing_market:
                print(f"Market '{market_data['name']}' already exists. Skipping.")
                existing_count += 1
            else:
                try:
                    # Create new market with common data
                    market = Market(
                        name=market_data["name"],
                        city="Yaoundé",
                        latitude=market_data["latitude"],
                        longitude=market_data["longitude"],
                        description="Marché local de Yaoundé"
                    )
                    db.session.add(market)
                    print(f"Market '{market_data['name']}' created successfully.")
                    created_count += 1
                except Exception as e:
                    print(f"Error creating market '{market_data['name']}': {e}")
                    db.session.rollback()
                    continue

        # Commit all changes
        try:
            db.session.commit()
            print(f"\nSeeding completed successfully!")
            print(f"Created: {created_count} markets")
            print(f"Already existed: {existing_count} markets")
            print(f"Total markets in database: {Market.query.count()}")
        except Exception as e:
            print(f"Error committing changes: {e}")
            db.session.rollback()

if __name__ == "__main__":
    seed_markets()