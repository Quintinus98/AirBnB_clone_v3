#!/usr/bin/python3
""" States Views """
from api.v1.views import app_views
from flask import jsonify, abort
from models.state import State
from models import storage


@app_views.route('/states', methods=["GET"], strict_slashes=False)
def all_states():
    """Returns a JSON"""
    states = storage.all(State).values()
    array = [state.to_dict() for state in states]
    return jsonify(array)


@app_views.route('/states/<state_id>', methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """Returns a JSON"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Returns a JSON"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return (jsonify({}), 200)
