from flask import Flask
from web_app.config import Config
from datetime import timedelta


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

    from web_app.app.blueprints.home import bp as home_bp
    from web_app.app.blueprints.users import bp as user_bp
    from web_app.app.blueprints.auth import bp as auth_bp
    from web_app.app.blueprints.categories import bp as category_bp
    from web_app.app.blueprints.products import bp as product_bp
    from web_app.app.blueprints.carts import bp as cart_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)

    # @app.teardown_appcontext
    # def close_db(error):
    #     storage.close()

    return app
