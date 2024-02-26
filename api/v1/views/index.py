#!/usr/bin/python3
""" Apps Index """
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from flask import jsonify
from models.place import Place
from models.review import Review
from models.state import State
from models import storage
from models.user import User


classes = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State, "users": User}


@app_views.route('/status', methods=["GET"])
def status():
    """Returns a JSON"""
    return jsonify({"status": "OK"}), 200


@app_views.route('/stats', methods=["GET"])
def count():
    """Retrieves the number of each objects by type"""
    tmp = {}
    for cls in classes:
        tmp[cls] = storage.count(classes[cls])
    return jsonify(tmp)
