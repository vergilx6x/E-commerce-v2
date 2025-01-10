from api.app.models.user import User
from api.app.models.product import Product
from api.app.models.cart import Cart
from api.app.models.cart_item import Cart_item
from api.app.models.order import Order
from api.app.models.order_item import Order_item
from api.app.models import storage
from api.app.blueprints import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/users/<user_id>/orders/<order_id>', methods=['GET'],
                 strict_slashes=False)
def get_order(order_id):
    """ Retrieves a specefic order."""
    order = storage.get(Order, order_id)

    if not order:
        abort(404)

    return jsonify(order.to_dict())


@app_views.route('/users/<user_id>/orders', methods=['GET'],
                 strict_slashes=False)
def get_orders(user_id):
    """ Gets the orders related to a user"""
    order = storage.get_order_by_user(user_id)

    if not order:
        abort(404)

    return jsonify(order.to_dict())


@app_views.route('/users/<user_id>/orders', methods=['POST'],
                 strict_slashes=False)
def post_order(user_id):
    """ Creates an order. """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user ID")

    data = request.get_json()

    data['user_id'] = user_id
    obj = Order(**data)
    obj.save()

    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/users/<user_id>/orders/<order_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_order(order_id):
    """ Deletes a specific order."""
    order = storage.get(Order, order_id)

    if not order:
        abort(404)

    storage.delete(order)
    storage.save()

    return make_response(jsonify({}), 200)
