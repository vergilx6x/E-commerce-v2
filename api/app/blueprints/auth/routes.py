import jwt
import datetime
from flask import request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from api.app.models.user import User  # Assuming a User model
from api.app.models import storage
from api.app.blueprints import app_views

# Register Route
@app_views.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if storage.get_user(username):
        return jsonify({"error": "Username already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password, email=email)
    storage.new(new_user)
    storage.save()

    return jsonify({"message": "User registered successfully"}), 201

# Login Route
@app_views.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = storage.get_user(username)
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)},
                       current_app.config['SECRET_KEY'], algorithm='HS256')
    refresh_token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)},
                               current_app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({"token": token, "refresh_token": refresh_token, "message": "Logged in successfully"}), 200

# Logout Route
@app_views.route('/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Logged out successfully"}), 200

# User Profile Route
@app_views.route('/user_profile', methods=['GET'])
def user_profile():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Missing authorization token"}), 401

    try:
        payload = jwt.decode(token.split(" ")[1], current_app.config['SECRET_KEY'], algorithms=['HS256'])
        user = storage.get(User, payload['user_id'])
        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"username": user.username, "user_id": user.id}), 200
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return jsonify({"error": "Invalid or expired token"}), 401

# Refresh Route for new access token
@app_views.route('/refresh', methods=['POST'])
def refresh():
    refresh_token = request.json.get('refresh_token')
    if not refresh_token:
        return jsonify({"error": "Refresh token missing"}), 400

    try:
        payload = jwt.decode(refresh_token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        user = storage.get(User, payload['user_id'])
        if not user:
            return jsonify({"error": "User not found"}), 404

        new_token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)},
                               current_app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({"token": new_token, "message": "Token refreshed successfully"}), 200
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return jsonify({"error": "Invalid or expired refresh token"}), 401
