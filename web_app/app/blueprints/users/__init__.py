from flask import Blueprint

# Initialize the blueprint for the products feature
bp = Blueprint('user', __name__)

from web_app.app.blueprints.users import routes