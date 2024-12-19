from api.app.models.cart import Cart
from api.app.models.user import User
from api.app.models.cart_item import Cart_item
from api.app.models import storage
from api.app.blueprints import app_views
from flask import abort, jsonify, make_response, request

@app_views.route('/carts', methods=['GET'], strict_slashes=False)
def get_carts():
    """ Retrieves all carts """
    all_carts = storage.all(Cart).values()
    list_carts = []
    
    for cart in all_carts:
        list_carts.append(cart.to_dict())
    
    return jsonify(list_carts)

@app_views.route('/carts/<cart_id>', methods=['GET'], strict_slashes=False)
def get_cart(cart_id):
    """ Retrieves a specefic cart."""
    cart = storage.get(Cart, cart_id)

    if not cart:
        abort(404)

    return jsonify(cart.to_dict())

@app_views.route('users/carts/<user_id>', methods=['GET'], strict_slashes=False)
def get_cart_by_user(user_id):
    """ Retrieves a specefic cart."""
    cart = storage.get_cart_by_user(user_id)

    if not cart:
        abort(404)

    return jsonify(cart.to_dict())

@app_views.route('/carts/<cart_id>', methods=['DELETE'], strict_slashes=False)
def delete_cart(cart_id):
    """Delete a cart"""
    cart = storage.get(Cart, cart_id)
    
    if not cart:
        abort(404)
        
    storage.delete(cart)
    storage.save()
    
    return make_response(jsonify({}), 200)


@app_views.route('carts/<cart_id>', methods=['POST'], strict_slashes=False)
def post_cart(user_id):
    """ Creates a cart."""
    cart = storage.get(cart, user_id)
    
    if not cart:
        abort(404)
    
    if not request.get_json():
        abort(400, description="Not a JSON")
    
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user ID")
    
    data = request.get_json()
    
    data['user_id'] = user_id
    obj = Cart(**data)
    obj.save()
    
    return make_response(jsonify(obj.to_dict()), 201)

@app_views.route('/carts/<cart_id>', methods=['PUT'], strict_slashes=False)
def put_cart(cart_id):
    """ Updates a Cart """
    cart = storage.get(Cart, cart_id)
    
    if not cart:
        abort(404)
        
    if not request.get_json():
        abort(400, description="Not a JSON")
    
    data = request.get_json()
    
    ignore = ['user_id', 'updated_at', 'created_at']
    
    for key, value in data.items():
        if key not in ignore:
            setattr(cart, key, value)
    
    storage.save()
    
    return make_response(jsonify(cart.to_dict()), 200)
