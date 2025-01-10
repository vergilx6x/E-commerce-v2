from flask import Blueprint

# Initialize the blueprint for the products feature
bp = Blueprint('auth', __name__)

from web_app.app.blueprints.auth import routes
