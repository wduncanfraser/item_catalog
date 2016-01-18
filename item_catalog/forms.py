from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, URL, Optional, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from item_catalog.models import Category


# Function to retrieve all active Categories
def get_categories():
    return Category.query.all()


# Form for creating/editing an Item
class ItemForm(Form):
    name = StringField('Name', validators=[DataRequired(), Length(max=128)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=256)])
    picture_url = StringField('Picture URL', validators=[URL(), Optional(), Length(max=256)])
    category = QuerySelectField('Category', query_factory=get_categories, allow_blank=False)
