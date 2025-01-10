#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api')

from api.app.blueprints.products.routes import *
from api.app.blueprints.categories.routes import *
from api.app.blueprints.users.routes import *
from api.app.blueprints.carts.routes import *
from api.app.blueprints.index import *
from api.app.blueprints.auth.routes import *
