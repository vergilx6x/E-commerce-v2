from api.app.models.user import User
from api.app.models import storage
from api.app.blueprints import app_views
from flask import abort, jsonify, make_response, request

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves all the user objects
    """
    all_users = storage.all(User).values()
    list_users = []
    for user in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)

@app_views.route('users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """retrieves an user """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    
    return jsonify(user.to_dict())

@app_views.route('users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes an user """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    
    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ Creates user """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    obj = User(**data)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """ 
    Updates an user object """
    user = storage.get(User, user_id)
    
    if not user:
        abort(404)
        
    if not request.get_json():
        abort(400, description="Not a JSON")
    
    ignore = ['id', 'email', 'created_at', 'updated_at']
    
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    
    storage.save()
    
    return make_response(jsonify(user.to_dict()), 200)

