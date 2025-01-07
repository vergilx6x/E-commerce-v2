from flask import Flask, render_template, make_response, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from api.app.models import storage
from api.app.blueprints import app_views
from os import environ
import os

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY', 'your_default_secret_key')  # Ensure JWT_SECRET_KEY is set properly
app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret_key')
# Initialize JWTManager
jwt = JWTManager(app)
app.register_blueprint(app_views)
CORS(app, supports_credentials=True)  # Allow co

@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """ Handle 404 error """
    return make_response(jsonify({'error': "Not found"}), 404)

if __name__ == "__main__":
    """ Main Function """
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = environ.get('HBNB_API_PORT', '5001')
    app.run(host=host, port=port, threaded=True, debug=True)
