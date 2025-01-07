
import requests
from flask import render_template, flash, redirect, url_for

from web_app.app.blueprints.products import bp as product_bp

@product_bp.route('/product/<string:product_id>')
def product_detail(product_id):
    # API endpoint to get the product details
    api_url = f"http://127.0.0.1:5001/api/products/{product_id}"
    
    try:
        # Make the request to the API to get the product data
        response = requests.get(api_url)
        
        if response.status_code == 200:
            product = response.json()  # Parse the product data from JSON response
            return render_template('product_detail.html', product=product)
        else:
            flash('Product not found.', 'error')
            return redirect(url_for('home.home'))
    
    except requests.exceptions.RequestException as e:
        flash(f"Error connecting to the API: {str(e)}", 'error')
        return redirect(url_for('home.home'))





