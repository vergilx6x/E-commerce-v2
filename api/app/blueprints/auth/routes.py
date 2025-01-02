from flask import Blueprint, request, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
from api.app.models.user import User
from api.app.models import storage
from api.app.blueprints import app_views
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity



# # Initialize JWT Manager (ensure app.config['JWT_SECRET_KEY'] is set)
# jwt = JWTManager()

@app_views.route('/register', methods=['POST'], strict_slashes=False)
def register_user():
    """Register a new user"""
    data = request.get_json()
    if not data:
        abort(400, description="Request body must be JSON")
    
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    if not email or not password or not username:
        abort(400, description="Missing required fields: email, password, username")
    
    if storage.get_user(username):
        abort(400, description="Username already exists")
    
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(email=email, username=username, password=hashed_password)
    storage.new(new_user)
    storage.save()
    return jsonify({"message": "User registered successfully"}), 201

@app_views.route('/login', methods=['POST'])
def login_user():
    """Authenticate user and return JWT"""
    data = request.get_json()
    if not data:
        abort(400, description="Request body must be JSON")
    
    username = data.get('username')
    password = data.get('password')
    user = storage.get_user(username)
    
    if user and check_password_hash(user.password, password):
        token = create_access_token(identity={"id": user.id, "username": user.username})
        return jsonify({"access_token": token}), 200
    return jsonify({"message": "Invalid username or password"}), 401

@app_views.route('/user_profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    """Get the authenticated user's profile"""
    identity = get_jwt_identity()
    user = storage.get(User, identity['id'])
    if not user:
        abort(404, description="User not found")
    
    return jsonify(user.to_dict()), 200

# @api_bp.route('/edit_profile', methods=['PUT'])
# @jwt_required()
# def edit_user_profile():
#     """Edit the authenticated user's profile"""
#     identity = get_jwt_identity()
#     user = storage.get(User, identity['id'])
#     if not user:
#         abort(404, description="User not found")
    
#     data = request.get_json()
#     user.email = data.get('email', user.email)
#     user.username = data.get('username', user.username)
#     user.first_name = data.get('first_name', user.first_name)
#     user.last_name = data.get('last_name', user.last_name)
    
#     storage.save()
#     return jsonify({"message": "Profile updated successfully"}), 200
