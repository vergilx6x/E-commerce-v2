from flask import Blueprint

# Initialize the blueprint for the products feature
bp = Blueprint('category', __name__)

from web_app.app.blueprints.categories import routes