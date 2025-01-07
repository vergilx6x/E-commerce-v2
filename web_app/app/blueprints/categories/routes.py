from flask import Blueprint, render_template, redirect, url_for, flash, request
from markupsafe import escape
# from web_app.models import storage
# from app.models.product import Product
# from app.models.category import Category
from urllib.request import urlopen
import json
import requests


from web_app.app.blueprints.categories import bp as category_bp


@category_bp.route('/home/category/<string:category_id>')
def category(category_id):
    # API endpoint to get the category details
    category_api_url = f"http://127.0.0.1:5001/api/categories/{category_id}"

    
    # API endpoint to get the products by category
    products_api_url = f"http://127.0.0.1:5001/api/categories/{category_id}/products"
    
    try:
        # Fetch category details from the API
        category_response = requests.get(category_api_url)
        
        # Check if category is found
        if category_response.status_code == 200:
            category = category_response.json()  # Get category details
            
            # Fetch products for the category from the API
            products_response = requests.get(products_api_url)
            
            if products_response.status_code == 200:
                products = products_response.json()  # List of products in the category
                return render_template('category.html', category=category, products=products)
            else:
                flash('Could not retrieve products. Please try again later.', 'error')
                return redirect(url_for('home.home'))
        else:
            flash('Category not found.', 'error')
            return redirect(url_for('home.home'))

    except requests.exceptions.RequestException as e:
        flash(f"Error connecting to the API: {str(e)}", 'error')
        return redirect(url_for('home.home'))