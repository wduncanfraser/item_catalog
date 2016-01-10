from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py', silent=True)

db = SQLAlchemy(app)


# Function to create initial database tables. this is done circularly to move models into a separate file.
def init_db():
    import item_catalog.models
    db.create_all()


# Import views. This is done circularly to move views into a separate file.
import item_catalog.views
