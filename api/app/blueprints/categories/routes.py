from api.app.models.product import Product
from api.app.models import storage
from api.app.blueprints import app_views
from api.app.models.category import Category
from flask import abort, jsonify, make_response, request

@app_views.route('/categories', methods=['GET'], strict_slashes=False)
def get_categories():
    """
    Retrieves a list of all categories """
    all_categories = storage.all(Category).values()
    list_categories = []
    for category in all_categories:
        list_categories.append(category.to_dict())
    
    return jsonify(list_categories)

@app_views.route('/categories/<category_id>', methods=['GET'], strict_slashes=False)
def get_category(category_id):
    """ Retrieves a specefic category"""
    category = storage.get(Category, category_id)
    if not category:
        abort(404)
    
    return jsonify(category.to_dict())

@app_views.route('/categories/<category_id>', methods=['DELETE'], strict_slashes=False)
def delete_category(category_id):
    """ Deletes a category """
    category = storage.get(Category, category_id)
    
    if not category:
        abort(404)
    
    storage.delete(category)
    storage.save()
    
    return make_response(jsonify({}), 200)

@app_views.route('/categories/<category_id>', methods=['POST'], strict_slashes=False)
def post_category():
    """Creates a category"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    
    data = request.get_json()
    obj = Category(**data)
    obj.save()
    
    return make_response(jsonify(obj.to_dict()), 201)

@app_views.route('/categories/<category_id>', methods=['PUT'], strict_slashes=False)
def put_category(category_id):
    """ Updates a category """
    category = storage.get(Category, category_id)
    
    if not category_id:
        abort(404)
        
    if not request.get_json():
        abort(400, description="Not a JSON")
    
    ignore = ['id', 'created_at', 'updated_at']
    
    data = request.get_json()
    
    for key, value in data.items():
        if key not in ignore:
            setattr(category, key, value)
    
    storage.save()
    
    return make_response(jsonify(category.to_dict()), 200)