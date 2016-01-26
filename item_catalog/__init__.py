from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.client import OAuth
from flask_wtf.csrf import CsrfProtect

# Create and configure flask app
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py', silent=True)
CsrfProtect(app)

# Setup Database instance
db = SQLAlchemy(app)

# Setup oauth and remote app
oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


# Function to create initial database tables. this is done circularly to move models into a separate file.
def init_db():
    import item_catalog.models
    db.create_all()


# Import views. This is done circularly to move views into a separate file.
import item_catalog.views
