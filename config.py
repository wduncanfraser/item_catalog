# Baseline Flask configuration used in production. Instance configuration is used to override specific settings.
# Sane default values for production
DEBUG = False
TESTING = False

# Values that need to overridden in instance configuration for production use, these values are sane defaults for
# development only
SECRET_KEY = 'development_key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/item_catalog.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
IMAGE_UPLOAD_DIRECTORY = '/home/vagrant/item_catalog/instance/images'
