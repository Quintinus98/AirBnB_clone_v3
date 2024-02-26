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


classes = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State, "users": User}


@app_views.route('/status', methods=["GET"])
def status():
    """Returns a JSON"""
    return jsonify({"status": "OK"}), 200


@app_views.route('/stats', methods=['GET'])
def number_objects():
    '''retrieves the number of each objects by type'''
    temp = {k: storage.count(v) for k, v in classes.items()}
    return jsonify(temp)
