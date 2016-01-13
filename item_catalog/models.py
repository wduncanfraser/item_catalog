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


# Category Model
class Category(db.Model):
    # Table Name
    __tablename__ = 'category'
    # Table Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)

    def __init__(self, name):
        self.name = name

    def __unicode__(self):
        return u'%s' % self.name


# Item Model
class Item(db.Model):
    # Table Name
    __tablename__ = 'item'
    # Table Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))
    picture_url = db.Column(db.String(256))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship(Category, backref='items')

    def __init__(self, name, description, picture_url, category):
        self.name = name
        self.description = description
        self.picture_url = picture_url
        self.category = category

    def __unicode__(self):
        return u'%s' % self.name
