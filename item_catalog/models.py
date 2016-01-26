from sqlalchemy import func
from flask import url_for
from item_catalog import db


# ---- Model Definitions ----#
# User and authentication models
# User model
class User(db.Model):
    # Table Name
    __tablename__ = 'user'
    # Table Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    picture = db.Column(db.String(256))
    google_id = db.Column(db.String(21), unique=True, nullable=True)

    def __unicode__(self):
        return u'%s' % self.name

    def __init__(self, name, email, picture=None, google_id=None):
        self.name = name
        self.email = email
        self.picture = picture
        self.google_id = google_id


# Category Model
class Category(db.Model):
    # Table Name
    __tablename__ = 'category'
    # Table Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)

    def __unicode__(self):
        return u'%s' % self.name

    def __init__(self, name=None):
        self.name = name

    @property
    def serialize(self):
        """Function that returns object data in easily serializeable format
        :return: Model fields in dict format"""
        return {
            'id': self.id,
            'name': self.name,
        }


# Item Model
class Item(db.Model):
    # Table Name
    __tablename__ = 'item'
    # Table Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024))
    picture = db.Column(db.String(256))
    edit_timestamp = db.Column(db.DateTime, default=func.now())
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship(Category, backref='items')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship(User, backref='items')

    def __unicode__(self):
        return u'%s' % self.name

    def __init__(self, name=None, description=None, category=None, owner=None):
        self.name = name
        self.description = description
        self.category = category
        self.owner = owner

    @property
    def serialize(self):
        """Function that returns object data in easily serializeable format
        :return: Model fields in dict format"""
        picture = url_for('item_image', item_id=self.id, _external=True) if self.picture else None
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'picture': picture
        }
