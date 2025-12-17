from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..extensions import db
from ..models import Market, User
from ..utils.decorators import login_required, role_required

markets = Blueprint('markets', __name__)

@markets.route('/markets')
@login_required
def list_markets():
    markets_list = Market.query.all()
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('market_list.html', markets=markets_list, user=user)

@markets.route('/markets/<int:id>')
@login_required
def market_detail(id):
    market = Market.query.get_or_404(id)
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('market_detail.html', market=market, user=user)

@markets.route('/markets/new', methods=['GET', 'POST'])
@role_required('admin')
def new_market():
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        description = request.form.get('description')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        if latitude:
            latitude = float(latitude)
        if longitude:
            longitude = float(longitude)
        market = Market(name=name, city=city, description=description, latitude=latitude, longitude=longitude)
        db.session.add(market)
        db.session.commit()
        flash('Market created successfully.')
        return redirect(url_for('markets.list_markets'))
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('market_form.html', user=user)

@markets.route('/markets/<int:id>/edit', methods=['GET', 'POST'])
@role_required('admin')
def edit_market(id):
    market = Market.query.get_or_404(id)
    if request.method == 'POST':
        market.name = request.form['name']
        market.city = request.form['city']
        market.description = request.form.get('description')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        if latitude:
            latitude = float(latitude)
        if longitude:
            longitude = float(longitude)
        market.latitude = latitude
        market.longitude = longitude
        db.session.commit()
        flash('Market updated successfully.')
        return redirect(url_for('markets.market_detail', id=id))
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('market_form.html', market=market, user=user)

@markets.route('/markets/<int:id>/delete', methods=['POST'])
@role_required('admin')
def delete_market(id):
    market = Market.query.get_or_404(id)
    db.session.delete(market)
    db.session.commit()
    flash('Market deleted successfully.')
    return redirect(url_for('markets.list_markets'))