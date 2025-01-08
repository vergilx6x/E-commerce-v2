from flask import render_template, session, redirect, url_for, flash, request
import requests

from web_app.app.blueprints.carts import bp as cart_bp
from web_app.app.blueprints.auth.routes import is_user_authenticated

BASE_API_URL = 'http://127.0.0.1:5001/api'

# Helper function to fetch user data
def fetch_user_data(token):
    response = requests.get(f"{BASE_API_URL}/user_profile", headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        return response.json()
    return None

# Helper function to fetch or create a cart
def fetch_or_create_cart(user_id):
    response = requests.get(f"{BASE_API_URL}/users/{user_id}/cart")
    if response.status_code == 404:
        create_response = requests.post(f"{BASE_API_URL}/users/{user_id}/cart", json={"user_id": user_id})
        if create_response.status_code == 201:
            return create_response.json()
        else:
            return None
    return response.json()

# Display the cart page
@cart_bp.route('/cart')
def cart():
    if not is_user_authenticated():
        flash('You need to log in to access the cart.', 'warning')
        return redirect(url_for('auth.login'))

    token = session.get('token')
    user_data = fetch_user_data(token)
    if not user_data:
        flash('Unable to fetch user information. Please log in again.', 'error')
        return redirect(url_for('auth.login'))

    user_id = user_data.get("user_id")
    cart_data = fetch_or_create_cart(user_id)

    if not cart_data:
        flash('Failed to fetch or create cart. Please try again later.', 'error')
        return redirect(url_for('auth.login'))

    cart_items_response = requests.get(f"{BASE_API_URL}/users/{user_id}/cart/cart-products")
    cart_items = cart_items_response.json() if cart_items_response.status_code == 200 else []

    if cart_items_response.status_code != 200:
        flash('Failed to fetch cart items. Please try again later.', 'error')

    return render_template('cart.html', cart_items=cart_items)

# Add a product to the cart
@cart_bp.route('/add_to_cart/<string:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if not is_user_authenticated():
        flash('You need to log in to add items to your cart.', 'warning')
        return redirect(url_for('auth.login'))

    token = session.get('token')
    user_data = fetch_user_data(token)
    if not user_data:
        flash('Unable to fetch user information. Please log in again.', 'error')
        return redirect(url_for('auth.login'))

    user_id = user_data.get("user_id")
    cart_data = fetch_or_create_cart(user_id)
    if not cart_data:
        flash('Failed to fetch or create cart. Please try again later.', 'error')
        return redirect(url_for('auth.login'))

    quantity = request.form.get('quantity', 1)
    payload = {'product_id': product_id, 'quantity': int(quantity)}
    print(payload)
    add_item_response = requests.post(f"{BASE_API_URL}/users/{user_id}/cart/cart-items", json=payload)

    if add_item_response.status_code == 201:
        flash('Product added to cart.', 'success')
    else:
        error_message = add_item_response.json().get('error', 'Failed to add product to cart.')
        flash(error_message, 'error')

    return redirect(url_for('cart.cart'))

@cart_bp.route('/remove_from_cart/<string:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if not is_user_authenticated():
        flash('You need to log in to remove items from your cart.', 'warning')
        return redirect(url_for('auth.login'))

    token = session.get('token')
    user_data = fetch_user_data(token)
    if not user_data:
        flash('Unable to fetch user information. Please log in again.', 'error')
        return redirect(url_for('auth.login'))

    user_id = user_data.get("user_id")
    cart_items_response = requests.get(f"{BASE_API_URL}/users/{user_id}/cart/cart-items")

    if cart_items_response.status_code != 200:
        flash('Failed to fetch cart items. Please try again later.', 'error')
        return redirect(url_for('cart.cart'))

    cart_items = cart_items_response.json()

    # Debug logging to verify the structure of cart_items
    print(product_id)
    print("Cart Items Retrieved:", cart_items)

    # Search for the cart item by product_id
    cart_item = next((item for item in cart_items if str(item.get('product_id')) == str(product_id)), None)

    if cart_item:
        cart_item_id = cart_item['id']
        delete_response = requests.delete(f"{BASE_API_URL}/users/{user_id}/cart/{cart_item_id}")
        if delete_response.status_code == 200:
            flash('Product removed from cart.', 'success')
        else:
            # Log the detailed error for debugging
            error_detail = delete_response.json().get('error', 'Unknown error')
            print("Error removing product:", error_detail)
            flash('Failed to remove product from cart. Please try again later.', 'error')
    else:
        flash(f'Product with ID {product_id} not found in cart.', 'error')

    return redirect(url_for('cart.cart'))

