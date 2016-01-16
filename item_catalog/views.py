from flask import render_template, abort
from item_catalog import app, db
from item_catalog.models import Category, Item, User


# Context processors
@app.context_processor
def get_categories():
    categories = Category.query.all()
    return dict(categories=categories)


# Default route, lists categories
@app.route('/category/')
@app.route('/')
def category_list():
    categories = Category.query.all()
    return render_template('category_list.html', categories=categories)


# Category view
@app.route('/category/<int:category_id>/')
def category_view(category_id):
    category = Category.query.filter_by(id=category_id).first_or_404()
    items = Item.query.filter_by(category=category).all()

    return render_template('category_view.html', category=category, items=items)


# Item View
@app.route('/item/<int:item_id>/')
@app.route('/category/<int:category_id>/item/<int:item_id>/')
def item_view(item_id, category_id=None):
    if category_id:
        category = Category.query.filter_by(id=category_id).first_or_404()
        item = Item.query.filter_by(id=item_id, category=category).first_or_404()
    else:
        category = None
        item = Item.query.filter_by(id=item_id).first_or_404()

    return render_template('item_view.html', category=category, item=item)
