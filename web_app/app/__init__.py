from flask import Flask
from web_app.config import Config

def create_app():
    app = Flask(__name__)
    # Load configuration from Config class
    app.config.from_object(Config)


    from web_app.app.blueprints.home import bp as home_bp
    from web_app.app.blueprints.users import bp as user_bp
    from web_app.app.blueprints.auth import bp as auth_bp
    from web_app.app.blueprints.categories import bp as category_bp
    from web_app.app.blueprints.products import bp as product_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(product_bp)

    # @app.teardown_appcontext
    # def close_db(error):
    #     storage.close()

    return app
