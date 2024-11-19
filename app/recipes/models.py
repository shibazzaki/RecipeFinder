from datetime import datetime

from app.extensions import db

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    steps = db.Column(db.Text, nullable=False)
    time_to_cook = db.Column(db.Integer, nullable=False)  # Час у хвилинах
    servings = db.Column(db.Integer, nullable=False)
    ingredients = db.relationship(
        'RecipeIngredient',
        back_populates='recipe',
        cascade='all, delete-orphan',  # Каскадне видалення
        lazy=True
    )
    favorites = db.relationship('FavoriteRecipe', back_populates='recipe', lazy=True)
    tried_recipes = db.relationship('TriedRecipe', back_populates='recipe', lazy=True)


class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    recipes = db.relationship('RecipeIngredient', back_populates='ingredient', lazy=True)

class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)
    recipe = db.relationship('Recipe', back_populates='ingredients')
    ingredient = db.relationship('Ingredient', back_populates='recipes')


class FavoriteRecipe(db.Model):
    __tablename__ = 'favorite_recipes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    user = db.relationship('User', back_populates='favorites')
    recipe = db.relationship('Recipe', back_populates='favorites')

class TriedRecipe(db.Model):
    __tablename__ = 'tried_recipes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='tried_recipes')
    recipe = db.relationship('Recipe', back_populates='tried_recipes')