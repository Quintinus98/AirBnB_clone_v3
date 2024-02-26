#!/usr/bin/python3
""" Cities Views"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.city import City
from models import storage
from models.state import State
from datetime import datetime
import uuid


@app_views.route("/states/<state_id>/cities", methods=["GET"])
@app_views.route("/states/<state_id>/cities/", methods=["GET"])
def all_cities(state_id):
    """Gets all cities"""
    cities = storage.all(City).values()
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if cities:
        for city in cities:
            city_array = [city.to_dict()]
        return jsonify(city_array)
    abort(404)


@app_views.route("/cities/<city_id>", methods=["GET"])
@app_views.route("/cities/<city_id>/", methods=["GET"])
def get_city(city_id):
    """Retrieves city object"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """"Delete a city"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return make_response((jsonify({})), 200)
    abort(404)


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def post_city(state_id):
    """Post a city"""
    states = storage.get(State, state_id)
    if not states:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data_request = request.get_json()
    if "name" not in data_request:
        abort(400, description="Missing name")
    data_request['state_id'] = state_id
    new_city = City(**data_request)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"])
def put_city(city_id):
    """Updates a city object"""
    city = storage.get(City, city_id)
    if city:
        if not request.is_json:
            abort(400, description="Not a Json")
        data_request = request.get_json()
        attr_ignore = ['id', 'state_id', 'created_at', 'updated_at']
        for k, v in data_request.items():
            if k not in attr_ignore:
                setattr(city, k, v)
            storage.save()
        return make_response(jsonify(city.to_dict()), 200)
    abort(404)
