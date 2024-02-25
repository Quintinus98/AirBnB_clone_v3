#!/usr/bin/python3
""" Apps Index """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=["GET"], strict_slashes=False)
def status():
    """Returns a JSON"""
    return jsonify({"status": "OK"}), 200


@app_views.route('/stats', methods=["GET"], strict_slashes=False)
def stats():
    """Retrieves endpoint"""
    classes = {"amenities": Amenity, "cities": City,
               "places": Place, "reviews": Review,
               "states": State, "users": User}
    template = {}
    for key, value in classes.items():
        template[key] = storage.count(value)
    return jsonify(template), 200
