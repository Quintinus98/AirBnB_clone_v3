#!/usr/bin/python3
""" Apps Index """
from api.v1.views import app_views
from flask import jsonify
import models

classes = {"amenities": "Amenity", "cities": "City", "places": "Place",
           "reviews": "Review", "states": "State", "users": "User"}


@app_views.route('/status', methods=["GET"])
def status():
    """Returns a JSON"""
    return jsonify({"status": "OK"}), 200


@app_views.route('/stats', methods=['GET'])
def count():
    '''retrieves the number of each objects by type'''
    count_dict = {}
    for cls in classes:
        count_dict[cls] = models.storage.count(classes[cls])
    return jsonify(count_dict)
