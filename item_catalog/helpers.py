import os
from item_catalog import app


# Saves uploaded file and returns path to be saved to model.
def save_uploaded_image(filename, data, item):
    directory_path = '/'.join([app.config['IMAGE_UPLOAD_DIRECTORY'], str(item.id)])
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    file_path = '/'.join([directory_path, filename])
    data.save(file_path)
    return '/'.join([str(item.id), filename])
