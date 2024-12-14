from api.app.models.product import Product
from api.app.models.category import Category
from api.app.models import storage
from api.app.blueprints import app_views
from flask import abort, jsonify, make_response, request

@app_views.route('/products', methods=['GET'], strict_slashes=False)
def get_products():
    """ Retrieves all products """
    all_products = storage.all(Product).values()
    list_products = []
    
    for product in all_products:
        list_products.append(product.to_dict()) 
        
    return jsonify(list_products)

@app_views.route('categories/<category_id>/products', methods=['GET'], strict_slashes=False)
def get_products_by_category(category_id):
    """ Retrieves all products of a specefic category """
    category = storage.get(Category, category_id)
    
    if not category:
        abort(404)
    
    products = [products.to_dict() for products in category.products]
    
    return jsonify(products)

@app_views.route('products/<product_id>', methods=['GET'], strict_slashes=False)
def get_product(product_id):
    """ Retrieves a specefic product """
    product = storage.get(Product, product_id)
    
    if not product:
        abort(404)
    
    return jsonify(product.to_dict())

@app_views.route('products/<product_id>', methods=['DELETE'], strict_slashes=False)
def delete_product(product_id):
    """ Retrieves a specefic product """
    product = storage.get(Product, product_id)
    
    if not product:
        abort(404)
        
    storage.delete(product)
    storage.save()
    
    return make_response(jsonify({}), 200)


@app_views.route('categories/<category_id>/products', methods=['POST'], strict_slashes=False)
def post_product(category_id):
    """ Creates a product """
    category = storage.get(Category, category_id)
    
    if not category:
        abort(404)
    
    if not request.get_json():
        abort(400, description="Not a JSON")
    
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    if 'price' not in request.get_json():
        abort(400, description="Missing price")
    
    data = request.get_json()
    
    data['category_id'] = category_id
    obj = Product(**data)
    obj.save()
    
    return make_response(jsonify(obj.to_dict()), 201)

@app_views.route('/products/<product_id>', methods=['PUT'], strict_slashes=False)
def put_product(product_id):
    """ Updates a Product """
    product = storage.get(Product, product_id)
    
    if not product:
        abort(404)
        
    if not request.get_json():
        abort(400, description="Not a JSON")
    
    data = request.get_json()
    
    ignore = ['category_id', 'updated_at', 'created_at']
    
    for key, value in data.items():
        if key not in ignore:
            setattr(product, key, value)
    
    storage.save()
    
    return make_response(jsonify(product.to_dict()), 200)
