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


classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review,
           "states": State, "users": User}


@app_views.route('/status')
def status():
    """Returns a JSON"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def retrieve_endpoint():
    """Retrieves endpoint"""
    template = {
        "amenities": 0,
        "cities": 0,
        "places": 0,
        "reviews": 0,
        "states": 0,
        "users": 0
    }
    for key, value in classes.items():
        total = storage.count(value)
        template[key] += total

    return jsonify(template)
