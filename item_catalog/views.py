from item_catalog import app


@app.route('/')
def hello_world():
    return 'Hello World!'