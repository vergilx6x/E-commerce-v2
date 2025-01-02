from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('web_app.config.Config')


    from web_app.app.blueprints.home import bp as home_bp
    from web_app.app.blueprints.users import bp as user_bp
    from web_app.app.blueprints.auth import bp as auth_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)

    # @app.teardown_appcontext
    # def close_db(error):
    #     storage.close()

    return app
