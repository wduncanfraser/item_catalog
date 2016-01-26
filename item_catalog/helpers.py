import os
from item_catalog import app, db
from item_catalog.models import User


# Saves uploaded file and returns path to be saved to model.
def save_uploaded_image(filename, data, item):
    """
    Function to save uploaded image for Item model
    :param filename: filename of the uploaded file
    :param data: picture data from the form
    :param item: item that the image is for
    :return: relative file name of the upload
    """
    directory_path = '/'.join([app.config['IMAGE_UPLOAD_DIRECTORY'], str(item.id)])
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    file_path = '/'.join([directory_path, filename])
    data.save(file_path)
    return '/'.join([str(item.id), filename])


# Get user by google id
def get_user_id(google_id):
    """
    Function to get user.id for specified google_id. Returns None if no user exists
    :param google_id: google id of user to look up
    :return: User.id
    """
    try:
        user = User.query.filter_by(google_id=google_id).one()
        return user.id
    except:
        return None


# Get user by ID.
def get_user(user_id):
    """
    Function to get User by id. Returns None if no user exists
    :param user_id: User.id of user
    :return: User instance or None
    """
    try:
        user = User.query.get(user_id)
        return user
    except:
        return None


# Create user from session data
def create_user(login_session):
    """
    Function to create new user. Returns existing user if a user with the same google_id already exists.
    :param login_session: Login session containing valid user data from google authentication
    :return: User instance, and boolean signifying whether the object was created
    """
    # Check if user exists first
    user_id = get_user_id(login_session.get('google_id'))
    if user_id:
        user = get_user(user_id)
        return user, False
    else:
        user = User(login_session.get('name'), login_session.get('email'), login_session.get('picture'), login_session.get('google_id'))
        db.session.add(user)
        db.session.commit()
        return user, True
