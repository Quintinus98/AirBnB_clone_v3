#!/usr/bin/python3
""" amenities Views """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from datetime import datetime
import uuid


@app_views.route('/amenities', methods=["GET"])
@app_views.route('/amenities/', methods=["GET"])
def all_amenities():
    """Gets all amenities"""
    amenities = storage.all(Amenity).values()
    array = [amenity.to_dict() for amenity in amenities]
    return jsonify(array)


@app_views.route('/amenities/<amenity_id>', methods=["GET"])
@app_views.route('/amenities/<amenity_id>/', methods=["GET"])
def get_amenity(amenity_id):
    """Gets an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=["DELETE"])
def delete_amenity(amenity_id):
    """Deletes an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=["POST"])
def create_amenity():
    """Posts an amenity"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    request_data = request.get_json()
    if "name" not in request_data:
        abort(400, description="Missing name")
    instance = Amenity(**request_data)
    storage.new(instance)
    storage.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=["PUT"])
def update_amenity(amenity_id):
    """Puts / Updates a amenitie"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")
    request_data = request.get_json()

    ignore_keys = ['id', 'created_at', 'updated_at']

    for k, v in request_data.items():
        if k not in ignore_keys:
            setattr(amenity, k, v)
    storage.save()
    return jsonify(amenity.to_dict()), 200
