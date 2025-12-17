"""
Routes pour la gestion des produits.

Gère les opérations CRUD sur les produits, y compris l'upload d'images.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort, current_app
from ..extensions import db
from ..models import Product, User, Market, Message
from ..utils.decorators import login_required, role_required
from ..services.product_service import create_product, update_product
from ..utils.validation_utils import validate_product_name, validate_product_price, validate_product_quantity

products = Blueprint('products', __name__)

@products.route('/products')
def list_products():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    # Rediriger les vendeurs vers leur catalogue personnel
    if user and user.role == 'seller':
        return redirect(url_for('products.my_products'))

    # Récupérer les paramètres de recherche et pagination
    name = request.args.get('name')
    market_id = request.args.get('market_id')
    price_min = request.args.get('price_min')
    price_max = request.args.get('price_max')
    page = request.args.get('page', 1, type=int)

    # Construire la requête avec filtres
    query = Product.query
    if name:
        query = query.filter(Product.name.ilike(f'%{name}%'))
    if market_id:
        query = query.filter(Product.market_id == int(market_id))
    if price_min:
        query = query.filter(Product.price >= float(price_min))
    if price_max:
        query = query.filter(Product.price <= float(price_max))

    # Pagination
    per_page = current_app.config.get('PER_PAGE', 12)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    products_list = pagination.items

    markets = Market.query.all()
    return render_template('all_products.html', products=products_list, markets=markets, user=user, pagination=pagination)

@products.route('/my-products')
@role_required('seller')
def my_products():
    user = User.query.get(session['user_id'])
    page = request.args.get('page', 1, type=int)

    # Pagination pour les produits du vendeur
    per_page = current_app.config.get('PER_PAGE', 12)
    pagination = Product.query.filter_by(seller_id=user.id).paginate(page=page, per_page=per_page, error_out=False)
    products_list = pagination.items

    return render_template('my_products.html', products=products_list, user=user, pagination=pagination)

@products.route('/products/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('product_detail.html', product=product, user=user)

@products.route('/products/new', methods=['GET', 'POST'])
@role_required('seller')
def new_product():
    """
    Affiche le formulaire de création de produit ou traite sa soumission.

    Pour les vendeurs uniquement. Gère l'upload d'image optionnel.
    """
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description')
        price_str = request.form['price']
        quantity_str = request.form.get('quantity')
        market_id = int(request.form['market_id'])
        seller_id = session['user_id']

        # Validation des données
        if not validate_product_name(name):
            return redirect(url_for('products.new_product'))
        price = validate_product_price(price_str)
        if price is None:
            return redirect(url_for('products.new_product'))
        quantity = validate_product_quantity(quantity_str)
        if quantity_str and quantity is None:  # Si quantité fournie mais invalide
            return redirect(url_for('products.new_product'))

        image_file = request.files.get('image') if 'image' in request.files else None
        create_product(name, description, price, quantity, market_id, seller_id, image_file)
        flash('Produit créé avec succès !', 'success')
        return redirect(url_for('products.my_products'))
    markets = Market.query.all()
    user = User.query.get(session['user_id'])
    return render_template('product_form.html', markets=markets, user=user)

@products.route('/products/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    """
    Affiche le formulaire d'édition de produit ou traite sa soumission.

    Vérifie que l'utilisateur est le propriétaire du produit.
    Permet la mise à jour de l'image.
    """
    product = Product.query.get_or_404(id)
    user = User.query.get(session['user_id'])
    if product.seller_id != user.id:
        abort(403)
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description')
        price_str = request.form['price']
        quantity_str = request.form.get('quantity')
        market_id = int(request.form['market_id'])

        # Validation des données
        if not validate_product_name(name):
            return redirect(url_for('products.edit_product', id=id))
        price = validate_product_price(price_str)
        if price is None:
            return redirect(url_for('products.edit_product', id=id))
        quantity = validate_product_quantity(quantity_str)
        if quantity_str and quantity is None:  # Si quantité fournie mais invalide
            return redirect(url_for('products.edit_product', id=id))

        image_file = request.files.get('image') if 'image' in request.files else None
        update_product(product, name, description, price, quantity, market_id, image_file)
        flash('Produit mis à jour avec succès !', 'success')
        return redirect(url_for('products.product_detail', id=id))
    markets = Market.query.all()
    return render_template('product_form.html', product=product, markets=markets, user=user)

@products.route('/products/<int:id>/delete', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    user = User.query.get(session['user_id'])
    if product.seller_id != user.id:
        abort(403)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully.')
    return redirect(url_for('products.my_products'))

@products.route('/products/<int:id>/contact', methods=['GET', 'POST'])
@login_required
def contact_seller(id):
    product = Product.query.get_or_404(id)
    user = User.query.get(session['user_id'])
    if user.role != 'buyer':
        abort(403)
    if product.seller_id == user.id:
        flash('Vous ne pouvez pas vous contacter vous-même.')
        return redirect(url_for('products.product_detail', id=id))
    if request.method == 'POST':
        content = request.form['content']
        message = Message(content=content, sender_id=user.id, receiver_id=product.seller_id, product_id=id)
        db.session.add(message)
        db.session.commit()
        flash('Message envoyé avec succès.')
        return redirect(url_for('products.product_detail', id=id))
    return render_template('contact_form.html', product=product, user=user)

@products.route('/messages')
@login_required
def messages():
    user = User.query.get(session['user_id'])
    if user.role == 'seller':
        messages_list = Message.query.filter_by(receiver_id=user.id).order_by(Message.created_at.desc()).all()
    else:
        messages_list = Message.query.filter_by(sender_id=user.id).order_by(Message.created_at.desc()).all()
    return render_template('messages.html', messages=messages_list, user=user)

@products.route('/products/<int:id>/chat')
@login_required
def chat(id):
    product = Product.query.get_or_404(id)
    user = User.query.get(session['user_id'])
    buyer_id = request.args.get('buyer_id', type=int)

    if user.role == 'buyer':
        if product.seller_id == user.id:
            abort(403)
        buyer = user
        seller = product.seller
    elif user.role == 'seller':
        if user.id != product.seller_id or not buyer_id:
            abort(403)
        buyer = User.query.get(buyer_id)
        seller = user
    else:
        abort(403)

    # Load messages
    messages_list = Message.query.filter(
        ((Message.sender_id == buyer.id) & (Message.receiver_id == seller.id) & (Message.product_id == id)) |
        ((Message.sender_id == seller.id) & (Message.receiver_id == buyer.id) & (Message.product_id == id))
    ).order_by(Message.created_at).all()

    return render_template('chat.html', product=product, messages=messages_list, user=user, buyer=buyer, seller=seller)
