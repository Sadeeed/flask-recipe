from flask import Flask
from flask_restful import Api

from apps.main.views import main as main_blueprint, RecipeList, RecipeView
from apps.auth.views import auth as auth_blueprint
from database import db
from flask_migrate import Migrate
from flask_login import LoginManager

# Models must be imported here for flask migrate to detect them
from apps.auth.models import User
from apps.main.models import Recipe, Ingredient, ingredients


def create_app():
    app = Flask(__name__)
    # setup with the configuration provided
    app.config.from_object('config.DevelopmentConfig')

    # setup all our dependencies
    db.init_app(app)
    Migrate(app, db)
    api = Api(app)

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

    # apis
    api.add_resource(RecipeList, '/api/recipe')
    api.add_resource(RecipeView, '/api/recipe/<recipe_id>')

    return app


if __name__ == "__main__":
    create_app().run()
