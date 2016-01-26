from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf.file import FileField, FileAllowed
from item_catalog.models import Category


# Function to retrieve all active Categories
def get_categories():
    """
    Function to retrieve all active Categories
    :return: List of all categories
    """
    return Category.query.all()


# Form for creating/editing an Item. Uses WTForms.
class ItemForm(Form):
    name = StringField('Name', validators=[DataRequired(), Length(max=128)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=1024)])
    picture = FileField('Picture', validators=[FileAllowed(['jpeg', 'jpg', 'png', 'gif'], 'Images only!')])
    category = QuerySelectField('Category', query_factory=get_categories, allow_blank=False)
