#!/usr/bin/python3
""" reviews API """
from models.review import Review
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def all_reviews(place_id):
    """Retrieves the list of all review objects"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    list_reviews = []
    for review in place.reviews:
        list_reviews.append(review.to_dict())
    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """
    Retrieves a Review object
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Deletes a Review Object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def post_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    request_data = request.get_json()
    user = storage.get(User, request_data['user_id'])
    if not user:
        abort(404)
    if 'text' not in request.get_json():
        abort(400, description="Missing text")
    request_data['place_id'] = place_id
    instance = Review(**request_data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_review(review_id):
    """Updates a Review"""
    review = storage.get(Review, review_id)

    if not review:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    request_data = request.get_json()
    for key, value in request_data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
