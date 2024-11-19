from flask import Flask
from .extensions import db, migrate, jwt, swagger
from .auth.controllers import auth_bp
from .jobs import backup_database
from .main.controllers import main_bp
from .recipes.controllers import recipes_bp
from app.extensions import db
from app.auth.models import User, Admin
from flask_admin import Admin
from .admin_views import AdminModelView  # Імпорт кастомного класу
from app.recipes.models import Recipe, Ingredient, RecipeIngredient, FavoriteRecipe, TriedRecipe
from flasgger import Swagger
from flask_apscheduler import APScheduler

scheduler = APScheduler()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Ініціалізація розширень
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    swagger.init_app(app)
    scheduler.init_app(app)
    scheduler.start()
    admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
    admin.add_view(AdminModelView(User, db.session))
    admin.add_view(AdminModelView(Recipe, db.session))
    admin.add_view(AdminModelView(Ingredient, db.session))
    admin.add_view(AdminModelView(FavoriteRecipe, db.session))
    admin.add_view(AdminModelView(TriedRecipe, db.session))

    scheduler.add_job(
        id='backup_database',
        func=backup_database,
        trigger='interval',
        minutes=60,  # Виконувати щогодини
    )

    # Реєстрація blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(recipes_bp, url_prefix='/recipes')
    app.register_blueprint(main_bp)  # Без префікса

    return app
