import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db
from ..models import User
from ..utils.validation_utils import validate_username, validate_email, validate_password

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # Validation des données
        if not validate_username(username):
            return redirect(url_for('auth.register'))
        if not validate_email(email):
            return redirect(url_for('auth.register'))
        if not validate_password(password):
            return redirect(url_for('auth.register'))

        # Vérifier si l'utilisateur existe déjà
        if User.query.filter_by(username=username).first():
            flash('Ce nom d\'utilisateur est déjà pris.', 'danger')
            return redirect(url_for('auth.register'))
        if User.query.filter_by(email=email).first():
            flash('Cette adresse email est déjà utilisée.', 'danger')
            return redirect(url_for('auth.register'))

        # Créer l'utilisateur
        password_hash = generate_password_hash(password)
        user = User(username=username, email=email, password_hash=password_hash, role=role)
        db.session.add(user)
        db.session.commit()
        current_app.logger.info(f"Nouvel utilisateur enregistré: {username} (rôle: {role})")
        flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['user_role'] = user.role
            session['username'] = user.username
            current_app.logger.info(f"Connexion réussie: {username} (rôle: {user.role})")
            flash('Connexion réussie !', 'success')
            if user.role == 'seller':
                return redirect(url_for('products.my_products'))
            elif user.role == 'admin':
                return redirect(url_for('markets.list_markets'))
            else:
                return redirect(url_for('products.list_products'))
        else:
            current_app.logger.warning(f"Tentative de connexion échouée: {username}")
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'danger')
            return redirect(url_for('auth.login'))
    return render_template('login.html')

@auth.route('/logout')
def logout():
    username = session.get('username', 'unknown')
    session.clear()
    current_app.logger.info(f"Déconnexion: {username}")
    flash('Logged out successfully')
    return redirect(url_for('main.index'))