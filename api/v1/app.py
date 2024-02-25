#!/usr/bin/python3
""" Apps API """
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


HBNB_API_HOST = getenv('HBNB_API_HOST')
HBNB_API_PORT = getenv('HBNB_API_PORT')

app = Flask(__name__)
app.url_map.strict_slashes = False

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage(exception):
    """Teardown storage"""
    storage.close()


if __name__ == "__main__":
    if not HBNB_API_HOST:
        HBNB_API_HOST = '0.0.0.0'
    if not HBNB_API_PORT:
        HBNB_API_PORT = 5000
    app.run(HBNB_API_HOST, HBNB_API_PORT, threaded=True, debug=True)
