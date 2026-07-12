import logging
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db
from ..models import User
from ..utils.validation_utils import validate_username, validate_email, validate_password

auth = Blueprint('auth', __name__)

# Initialiser le limiteur de taux pour la prévention des attaques par force brute
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Décorateur pour vérifier si l'utilisateur est authentifié
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Veuillez vous connecter d\'abord.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per hour")
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        role = request.form.get('role', 'buyer')
        
        # Vérifier que tous les champs sont remplis
        if not all([username, email, password, password_confirm]):
            flash('Tous les champs sont obligatoires.', 'danger')
            return render_template('register.html')
        
        # Vérifier que les mots de passe correspondent
        if password != password_confirm:
            flash('Les mots de passe ne correspondent pas.', 'danger')
            return render_template('register.html')
        
        # Validation des données
        if not validate_username(username):
            flash('Le nom d\'utilisateur n\'est pas valide. Il doit contenir entre 3 et 20 caractères.', 'danger')
            return render_template('register.html')
        
        if not validate_email(email):
            flash('L\'adresse email n\'est pas valide.', 'danger')
            return render_template('register.html')
        
        if not validate_password(password):
            flash('Le mot de passe n\'est pas assez fort. Il doit contenir au moins 8 caractères.', 'danger')
            return render_template('register.html')
        
        # Vérifier si l'utilisateur existe déjà
        if User.query.filter_by(username=username).first():
            flash('Ce nom d\'utilisateur est déjà pris.', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Cette adresse email est déjà utilisée.', 'danger')
            return render_template('register.html')
        
        # Valider le rôle
        valid_roles = ['buyer', 'seller', 'admin']
        if role not in valid_roles:
            role = 'buyer'
        
        try:
            # Créer l'utilisateur
            password_hash = generate_password_hash(password, method='pbkdf2:sha256')
            user = User(username=username, email=email, password_hash=password_hash, role=role)
            db.session.add(user)
            db.session.commit()
            current_app.logger.info(f"Nouvel utilisateur enregistré: {username} (rôle: {role})")
            flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Erreur lors de l'enregistrement: {str(e)}")
            flash('Une erreur est survenue lors de l\'enregistrement. Veuillez réessayer.', 'danger')
            return render_template('register.html')
    
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per hour")
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Vérifier que tous les champs sont remplis
        if not username or not password:
            flash('Nom d\'utilisateur et mot de passe requis.', 'danger')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            # Mettre à jour la session
            session['user_id'] = user.id
            session['user_role'] = user.role
            session['username'] = user.username
            session.permanent = True  # Rendre la session persistante
            
            current_app.logger.info(f"Connexion réussie: {username} (rôle: {user.role})")
            flash('Connexion réussie !', 'success')
            
            # Redirection basée sur le rôle
            if user.role == 'seller':
                return redirect(url_for('products.my_products'))
            elif user.role == 'admin':
                return redirect(url_for('markets.list_markets'))
            else:
                return redirect(url_for('products.list_products'))
        else:
            current_app.logger.warning(f"Tentative de connexion échouée: {username}")
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'danger')
            return render_template('login.html')
    
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    username = session.get('username', 'unknown')
    session.clear()
    current_app.logger.info(f"Déconnexion: {username}")
    flash('Déconnexion réussie !', 'success')
    return redirect(url_for('main.index'))
