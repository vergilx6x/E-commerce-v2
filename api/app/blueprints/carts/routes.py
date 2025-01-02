from api.app.models.cart import Cart
from api.app.models.user import User
from api.app.models.product import Product
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


@app_views.route('users/<user_id>/cart',
                 methods=['GET'], strict_slashes=False)
def get_cart_by_user(user_id):
    """ Retrieves a specefic cart."""
    cart = storage.get_cart_by_user(user_id)

    if not cart:
        abort(404)

    return jsonify(cart.to_dict())


# @app_views.route('/carts/<cart_id>', methods=['DELETE'], strict_slashes=False)
# def delete_cart(cart_id):
#     """Delete a cart"""
#     cart = storage.get(Cart, cart_id)

#     if not cart:
#         abort(404)

#     storage.delete(cart)
#     storage.save()

#     return make_response(jsonify({}), 200)


@app_views.route('/users/<user_id>/cart', methods=['DELETE'], strict_slashes=False)
def delete_cart(cart_id):
    """Delete a cart"""
    cart = storage.get(Cart, cart_id)

    if not cart:
        abort(404)

    storage.delete(cart)
    storage.save()

    return make_response(jsonify({}), 200)


# @app_views.route('carts/<cart_id>', methods=['POST'], strict_slashes=False)
# def post_cart(user_id):
#     """ Creates a cart."""
#     if not request.get_json():
#         abort(400, description="Not a JSON")

#     if 'user_id' not in request.get_json():
#         abort(400, description="Missing user ID")

#     data = request.get_json()

#     data['user_id'] = user_id
#     obj = Cart(**data)
#     obj.save()

#     return make_response(jsonify(obj.to_dict()), 201)


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


@app_views.route('/users/<user_id>/cart', methods=['POST'], strict_slashes=False)
def post_cart(user_id):
    """ Post a cart related to an user. """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user ID")

    data = request.get_json()

    data['user_id'] = user_id
    obj = Cart(**data)
    obj.save()

    return make_response(jsonify(obj.to_dict()), 201)    

# This is the cart items part.

@app_views.route('/users/<user_id>/cart/cart-items',
                 methods=['GET'], strict_slashes=False)
def get_cart_items(user_id):
    """ Gets cart items"""
    cart = storage.get_cart_by_user(user_id)
    cart_items = storage.all(Cart_item).values()
    list_cart_items = []

    if not cart_items:
        abort(404)

    for item in cart_items:
        if item.cart_id == cart.id:
            list_cart_items.append(item.to_dict())

    return jsonify(list_cart_items)

@app_views.route('/users/<user_id>/cart/<cart_item_id>', methods=['GET'], strict_slashes=False)
def get_cart_item(user_id, cart_id):
    """ Get a specific cart item. """ 
    cart_item = storage.get(Cart_item, cart_id)

    if not cart_item:
        abort(404)

    return jsonify(cart_item.to_dict())


@app_views.route('/users/<user_id>/cart/cart-items', methods=['POST'], strict_slashes=False)
def post_cart_item(user_id):
    """ Post a cart item."""
    cart = storage.get_cart_by_user(user_id)

    if not cart:
        abort(404, description="Cart not found")

    if 'product_id' not in request.get_json():
        abort(400, description="Missing product id")
    if 'quantity' not in request.get_json():
        abort(400, description="Missing quantity")
    
    data = request.get_json()

    product = storage.get(Product, data['product_id'])
    if not product:
        abort(404, description="Product not found")

    if product.quantity < data['quantity']:
        abort(400, description="Insufficient stock for the requested quantity")

    existing_item = next(
        (item for item in cart.cart_items if item.product_id == product.id), None
    )
    if existing_item:
        # Update quantity if the product already exists in the cart
        existing_item.quantity += data['quantity']
        obj = existing_item
    else:
        # Create a new cart item
        data['cart_id'] = cart.id
        obj = Cart_item(**data)
        obj.save()

    # Update product stock
    product.quantity -= data['quantity']
    product.save()
    
    return make_response(jsonify(obj.to_dict()), 201)
