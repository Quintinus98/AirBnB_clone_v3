#!/usr/bin/python3
""" States Views """
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states', methods=['GET'])
def all_states():
    """Gets all States"""
    states = storage.all(State).values()
    list_states = []
    for state in states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Gets a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'])
def post_state():
    """Posts a State"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    request_data = request.get_json()
    obj = State(**request_data)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=["PUT"])
def put_state(state_id):
    """Puts / Updates a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'created_at', 'updated_at']
    request_data = request.get_json()
    for k, v in request_data.items():
        if k not in ignore_keys:
            setattr(state, k, v)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
