from flask import render_template, redirect, url_for, abort, flash
from item_catalog import app, db
from item_catalog.models import Category, Item, User
from item_catalog.forms import ItemForm


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
    category = Category.query.get_or_404(category_id)
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


# New Item
@app.route('/item/new', methods=['GET', 'POST'])
def item_new():
    form = ItemForm()

    if form.validate_on_submit():
        item = Item()
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        flash("Succesfully Created %s" % item.name, 'notice')
        return redirect(url_for('item_view', item_id=item.id))

    return render_template('item_edit.html', form=form)


# Edit Item
@app.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
def item_edit(item_id):
    item = Item.query.get_or_404(item_id)
    form = ItemForm(obj=item)

    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        flash("Succesfully Saved %s" % item.name, 'notice')
        return redirect(url_for('item_view', item_id=item.id))

    return render_template('item_edit.html', form=form, item=item)
