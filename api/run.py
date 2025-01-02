#!/usr/bin/python3
""" Flask Application """
from api.app.models import storage
from api.app.blueprints import app_views
from os import environ
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key

# Initialize JWTManager
jwt = JWTManager(app)
app.register_blueprint(app_views)
# cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
cors = CORS(app)


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)



if __name__ == "__main__":
    """ Main Function """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5001'
    app.run(host=host, port=port, threaded=True, debug=True)
