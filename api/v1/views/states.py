#!/usr/bin/python3
""" States Views """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route('/states/', methods=["GET"])
def all_states():
    """Gets all States"""
    states = storage.all(State).values()
    array = [state.to_dict() for state in states]
    return jsonify(array)


@app_views.route('/states/<state_id>', methods=["GET"])
def get_state(state_id):
    """Gets a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=["DELETE"])
def delete_state(state_id):
    """Deletes a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=["POST"])
def post_state():
    """Posts a State"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    request_data = request.get_json()
    if "name" not in request_data:
        abort(400, description="Missing name")
    instance = State(**request_data)
    storage.new(instance)
    storage.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/states/<state_id>', methods=["PUT"])
def put_state(state_id):
    """Puts / Updates a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")
    request_data = request.get_json()

    ignore_keys = ['id', 'created_at', 'updated_at']

    for k, v in request_data.items():
        if k not in ignore_keys:
            setattr(state, k, v)
    storage.save()
    return jsonify(state.to_dict()), 200
