from flask import Flask
from apps.main.views import main as main_blueprint
from apps.auth.views import auth as auth_blueprint
from database import db
from flask_login import LoginManager
from apps.auth.models import User


def create_app():
    app = Flask(__name__)
    # setup with the configuration provided
    app.config.from_object('config.DevelopmentConfig')

    # setup all our dependencies
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.signin'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # register blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    return app


if __name__ == "__main__":
    create_app().run()
