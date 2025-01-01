from flask import Blueprint

# Initialize the blueprint for the products feature
bp = Blueprint('home', __name__)

from web_app.app.blueprints.home import routes