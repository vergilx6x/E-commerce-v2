from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from markupsafe import escape
from urllib.request import urlopen
import json
import requests

from web_app.app.blueprints.home import bp as home_bp

API_URL = 'http://127.0.0.1:5001/api/v1'

@home_bp.route('/home', strict_slashes=False)
@home_bp.route('/', strict_slashes=False)
# # def home():
# #     # Fetch categories from the API
# #     try:
# #         with urlopen(f'{API_URL}/categories') as response:
# #             categories = json.loads(response.read().decode())
# #     except Exception as e:
# #         categories = []  # Handle API failure gracefully
# #         print(f"Error fetching categories: {e}")

# #     # Fetch products from the API
# #     try:
# #         with urlopen(f'{API_URL}/products') as response:
# #             all_products = json.loads(response.read().decode())
# #     except Exception as e:
# #         all_products = []  # Handle API failure gracefully
# #         print(f"Error fetching products: {e}")

# #     # Sort products by 'created_at' field, descending
# #     all_products.sort(key=lambda p: p['created_at'], reverse=True)

# #     # Get the 10 most recent products
# #     new_products = all_products[:10]

# #     return render_template('home.html', categories=categories, new_products=new_products, all_products=all_products)

# def home():
#     categories = storage.all(Category).values()
#     all_products = list(storage.all(Product).values())
#     all_products.sort(key=lambda p: p.created_at, reverse=True)
#     new_products = all_products[:10]

#     return render_template('home.html', categories=categories, new_products=new_products, all_products=all_products)

# @home_bp.route('/home/category/<string:category_id>')
# def category(category_id):
#     category = storage.get(Category, category_id)
#     if category:
#         products = [product for product in storage.all(Product).values() if product.category_id == category_id]
#         return render_template('category.html', category=category, products=products)
#     else:
#         flash('Category not found.', 'error')
#         return redirect(url_for('home.home'))




def home():
    cart = []
    # Fetch categories from the API
    categories_response = requests.get(f"http://127.0.0.1:5001/api/categories")
    categories = categories_response.json() if categories_response.status_code == 200 else []

    # Fetch products from the API
    products_response = requests.get(f"http://127.0.0.1:5001/api/new_products")
    products = products_response.json() if products_response.status_code == 200 else []

    return render_template('index.html', products=products, categories=categories)

@home_bp.route('/shop', strict_slashes=False)
def shop():
    cart = []
    # Fetch categories from the API
    categories_response = requests.get(f"http://127.0.0.1:5001/api/categories")
    categories = categories_response.json() if categories_response.status_code == 200 else []

    # Fetch products from the API
    products_response = requests.get(f"http://127.0.0.1:5001/api/products")
    products = products_response.json() if products_response.status_code == 200 else []

    return render_template('shop.html', products=products, categories=categories)

@home_bp.route('/add_to_cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    # Add to cart functionality (you can connect this to your API or database)
    return jsonify({"message": f"Product {item_id} added to cart!"}), 200

@home_bp.route('/about', strict_slashes=False)
def about():


    return render_template('about.html')



@home_bp.route('/contact', strict_slashes=False)
def contact():
    

    return render_template('contact.html')