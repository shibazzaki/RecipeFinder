from flask import Blueprint, request
from app.recipes.services import create_recipe, get_recipes, delete_recipe

recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('/', methods=['POST'])
def add_recipe():
    data = request.get_json()
    return create_recipe(data)

@recipes_bp.route('/', methods=['GET'])
def list_recipes():
    return get_recipes()

@recipes_bp.route('/<int:recipe_id>', methods=['DELETE'])
def remove_recipe(recipe_id):
    return delete_recipe(recipe_id)
