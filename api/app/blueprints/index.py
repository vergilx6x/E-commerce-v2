#!/usr/bin/python3
""" Index """
from api.app.models.cart import Cart
from api.app.models.cart_item import Cart_item
from api.app.models.category import Category
from api.app.models.favorite import Favorite
from api.app.models.order import Order
from api.app.models.order_item import Order_item
from api.app.models.product import Product
from api.app.models import storage
from api.app.blueprints import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Retrieves the number of each objects by type """
    classes = [Cart, Cart_item, Category, Favorite, Order, Order_item, Product]
    names = ["Cart", "Cart_item", "Category", "Favorite", "Order", "Order_item", "Product"]

    num_objs = {}
    for i in range(len(classes)):
        num_objs[names[i]] = storage.count(classes[i])

    return jsonify(num_objs)