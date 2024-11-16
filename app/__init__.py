from flask import Flask
from .extensions import db, migrate, jwt, swagger
from .auth.controllers import auth_bp
from .recipes.controllers import recipes_bp
from app.extensions import db
from app.auth.models import User, Admin
from app.recipes.models import Recipe, Ingredient, RecipeIngredient, FavoriteRecipe
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Ініціалізація розширень
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    swagger.init_app(app)

    # Реєстрація blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(recipes_bp, url_prefix='/recipes')

    return app
