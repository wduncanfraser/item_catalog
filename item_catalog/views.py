from flask import render_template, redirect, url_for, abort, flash, request, jsonify, send_from_directory, session
from werkzeug.contrib.atom import AtomFeed
from werkzeug.utils import secure_filename
from datetime import datetime
import httplib2
from item_catalog import app, db, google
from item_catalog.models import Category, Item, User
from item_catalog.forms import ItemForm
from item_catalog.helpers import save_uploaded_image, get_user_id, get_user, create_user, check_login, is_item_owner


# ----Account views----#
# Context Processor
@app.context_processor
def context_check_login():
    """
    Context processor to check if a user is logged in.
    :return: dict containing boolean signifying if there is a logged in user and instance of the user
    """
    logged_in = check_login(session)
    user = None

    if logged_in:
        user = get_user(session.get('user_id'))

    return dict(logged_in=logged_in, user=user)


# Login View
@app.route('/login')
def login():
    """
    Login view. Redirects to google authorization
    """
    return google.authorize(callback=url_for('authorized', _external=True))


# Logout View
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    Logout view. Revokes token and purges all login data from session.
    """
    if not session.get('google_token'):
        flash('No User to Sign Out', 'warning')
        return redirect(url_for('category_list'))

    if request.method == 'POST':
        # Attempt to revoke oauth token
        url = '%s%s' % (app.config['GOOGLE_REVOKE_URL'], session['google_token'][0])
        h = httplib2.Http()
        result = h.request(url, 'GET')[0]

        # Clear session
        session.pop('google_token', None)
        session.pop('google_id', None)
        session.pop('name', None)
        session.pop('email', None)
        session.pop('picture', None)
        session.pop('user_id', None)

        if result['status'] == '200':
            flash('Successfully Signed Out', 'notice')
        else:
            flash('Successfully Signed Out', 'notice')
            flash('Failed to Revoke Google OAuth Token', 'error')

        return redirect(url_for('category_list'))

    return render_template('logout.html')


# View for handling authorization
@app.route('/login/authorized')
def authorized():
    """
    Authorization return for OAuth. Populates session data on login. Creates or retrieves user based on google_id and
    syncs user data with data provided by google.
    """
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    user_info = google.get('userinfo')
    session['google_id'] = user_info.data['id']
    session['name'] = user_info.data['name']
    session['email'] = user_info.data['email']
    session['picture'] = user_info.data['picture']
    # Get or create user and add the user_id to the session
    session['user_id'] = get_user_id(session['google_id']) or create_user(session)[0].id
    # Sync user data from google
    user = get_user(session['user_id'])
    user.name = session['name']
    user.email = session['email']
    user.picture = session['picture']
    db.session.add(user)
    db.session.commit()

    flash('Signed in as %s' % session['name'], 'notice')
    return redirect(url_for('category_list'))


# Google token getter
@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


# ----Item Catalog CRUD Views----#
# Context processor
@app.context_processor
def context_get_categories():
    """
    Context processor to make all categories available.
    :return: dict containing list of all categories
    """
    categories = Category.query.all()
    return dict(categories=categories)


# Default route, lists categories
@app.route('/category/')
@app.route('/')
def category_list():
    """
    View rendering list of all categories and recently added items.
    :context recent_items: list of instance of :model:`item_catalog.Item`
    :template: `category_list.html`
    """
    recent_items = Item.query.order_by(Item.id.desc()).limit(10).all()
    return render_template('category_list.html', recent_items=recent_items)


# Return category list as JSON
@app.route('/category/JSON')
def category_list_json():
    """
    View returning JSON of all categories.
    :rtype: JSON
    """
    categories = Category.query.all()
    return jsonify(categories=[category.serialize for category in categories])


# Category view
@app.route('/category/<int:category_id>/')
def category_view(category_id):
    """
    View returning list of all items in a specific category.
    :param category_id: id of the requested category
    :context category: Instance of :model:`item_catalog.Category`
    :template: `category_view.html`
    """
    category = Category.query.get_or_404(category_id)
    items = Item.query.filter_by(category=category).all()
    return render_template('category_view.html', category=category, items=items)


# Return category as JSON
@app.route('/category/<int:category_id>/JSON')
def category_view_json(category_id):
    """
    View returning JSON of category and all items in category
    :param category_id: id of the requested category
    :rtype: JSON
    """
    category = Category.query.get_or_404(category_id)
    items = Item.query.filter_by(category=category).all()

    return jsonify(category=category.serialize, items=[item.serialize for item in items])


# Return feed of recent items
@app.route('/atom')
def recent_items_atom():
    """
    View returning ATOM Feed of recently added items
    :rtype: AtomFeed
    """
    feed = AtomFeed('Recent Items', feed_url=request.url, url=request.url_root, author="W. Duncan Fraser")
    items = Item.query.order_by(Item.id.desc()).limit(10).all()

    for item in items:
        feed.add(item.name, unicode(item.description), content_type='html', id=item.id, updated=item.edit_timestamp)

    return feed.get_response()


# Item View
@app.route('/item/<int:item_id>/')
@app.route('/category/<int:category_id>/item/<int:item_id>/')
def item_view(item_id, category_id=None):
    """
    View to view all details of specified item.
    :param item_id: id of requested item
    :param category_id: optional, id of category of requested item
    :context category: Instance of :model:`item_catalog.Category`
    :context item: Instance of :model:`item_catalog.Item`
    :template: `item_view.html`
    """
    if category_id:
        category = Category.query.get_or_404(category_id)
        item = Item.query.filter_by(id=item_id, category=category).first_or_404()
    else:
        category = None
        item = Item.query.get_or_404(item_id)

    # Check if user is owner
    owner = check_login(session) and is_item_owner(item, session.get('user_id'))

    return render_template('item_view.html', category=category, item=item, owner=owner)


# Item Image View
@app.route('/item/<int:item_id>/image')
def item_image(item_id):
    """
    View for rendering item image.
    :param item_id: id of requested item image
    :return: image
    """
    item = Item.query.get_or_404(item_id)
    return send_from_directory(app.config['IMAGE_UPLOAD_DIRECTORY'], item.picture)


# Return item as JSON
@app.route('/item/<int:item_id>/JSON')
@app.route('/category/<int:category_id>/item/<int:item_id>/JSON')
def item_view_json(item_id, category_id=None):
    """
    View returning JSON of specified item and associated category
    :param item_id: id of requested item
    :param category_id: optional, id of category of requested item
    :rtype: JSON
    """
    if category_id:
        category = Category.query.get_or_404(category_id)
        item = Item.query.filter_by(id=item_id, category=category).first_or_404()
    else:
        item = Item.query.get_or_404(item_id)

    return jsonify(item=item.serialize, category=item.category.serialize)


# New Item
@app.route('/item/new', methods=['GET', 'POST'])
@app.route('/category/<int:category_id>/item/new/', methods=['GET', 'POST'])
def item_new(category_id=None):
    """
    View for creating new item
    :param category_id: optional, id of category of new item
    :context form: Instance of :form:`item_catalog.ItemForm`
    :template: `item_edit.html`
    """
    # Check if user is logged in
    if not check_login(session):
        abort(403)

    if category_id:
        category = Category.query.get_or_404(category_id)
    else:
        category = None

    form = ItemForm()

    # If form is valid on post, populate model instance and save
    if form.validate_on_submit():
        item = Item()
        form.populate_obj(item)
        item.picture = None
        item.owner = User.query.get(session.get('user_id'))
        db.session.add(item)
        db.session.commit()

        # If there is picture data, let's save it now that we have an item id
        if form.picture.data:
            data = form.picture.data
            filename = secure_filename(data.filename)
            item_path = None
            try:
                item_path = save_uploaded_image(filename, data, item)
            except:
                abort(500)

            item.picture = item_path
            db.session.add(item)
            db.session.commit()

        flash("Successfully Created %s" % item.name, 'notice')
        return redirect(url_for('item_view', item_id=item.id))

    return render_template('item_edit.html', form=form, category=category)


# Edit Item
@app.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
def item_edit(item_id):
    """
    View for editing an existing item. Check if current user is owner. Aborts otherwise.
    :param item_id: id of requested item
    :context form: Instance of :form:`item_catalog.ItemForm`
    :context item: Instance of :model:`item_catalog.Item`
    :template: `item_edit.html`
    """
    item = Item.query.get_or_404(item_id)

    # Check if user is logged in and the item owner. Abort if either check fails
    if not check_login(session) or not is_item_owner(item, session.get('user_id')):
        abort(403)

    form = ItemForm(obj=item)

    if form.validate_on_submit():
        item_path = item.picture

        if form.picture.data:
            data = form.picture.data
            filename = secure_filename(data.filename)
            try:
                item_path = save_uploaded_image(filename, data, item)
            except:
                abort(500)

        form.populate_obj(item)
        item.picture = item_path
        item.edit_timestamp = datetime.utcnow()
        db.session.add(item)
        db.session.commit()
        flash("Successfully Saved %s" % item.name, 'notice')
        return redirect(url_for('item_view', item_id=item.id))

    return render_template('item_edit.html', form=form, item=item)


# Delete Item
@app.route('/item/<int:item_id>/delete', methods=['GET', 'POST'])
def item_delete(item_id):
    """
    View for deleting an existing item. Check if current user is owner. Aborts otherwise.
    :param item_id: id of requested item
    :context item: Instance of :model:`item_catalog.Item`
    :template: `item_delete.html`
    """
    item = Item.query.get_or_404(item_id)

    # Check if user is logged in and the item owner. Abort if either check fails
    if not check_login(session) or not is_item_owner(item, session.get('user_id')):
        abort(403)

    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        flash("Successfully Deleted %s" % item.name, 'notice')
        return redirect(url_for('category_view', category_id=item.category_id))

    return render_template('item_delete.html', item=item)
