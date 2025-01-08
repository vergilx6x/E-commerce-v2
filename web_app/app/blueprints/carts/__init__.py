from flask import Blueprint

# Initialize the blueprint for the products feature
bp = Blueprint('cart', __name__)

from web_app.app.blueprints.carts import routes