#!/usr/bin/python3
""" Apps API """
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv


HBNB_API_HOST = getenv('HBNB_API_HOST')
HBNB_API_PORT = getenv('HBNB_API_PORT')

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage(exception):
    """Teardown storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Error handler"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    if not HBNB_API_HOST:
        HBNB_API_HOST = '0.0.0.0'
    if not HBNB_API_PORT:
        HBNB_API_PORT = 5000
    app.run(HBNB_API_HOST, HBNB_API_PORT, threaded=True, debug=True)
