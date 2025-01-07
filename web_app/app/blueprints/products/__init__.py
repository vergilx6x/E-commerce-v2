from flask import Blueprint

# Initialize the blueprint for the products feature
bp = Blueprint('product', __name__)

from web_app.app.blueprints.products import routes