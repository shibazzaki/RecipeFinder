from flask import Blueprint, request
from app.recipes.services import create_recipe, get_recipes, delete_recipe, add_to_favorites, remove_from_favorites, \
    get_favorites, filter_recipes

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

@recipes_bp.route('/favorites', methods=['POST'])
def add_favorite():
    data = request.get_json()
    user_id = data.get('user_id')  # У реальному додатку user_id береться з токена
    recipe_id = data.get('recipe_id')
    return add_to_favorites(user_id, recipe_id)

@recipes_bp.route('/favorites/<int:recipe_id>', methods=['DELETE'])
def remove_favorite(recipe_id):
    user_id = request.args.get('user_id')  # У реальному додатку user_id береться з токена
    return remove_from_favorites(user_id, recipe_id)

@recipes_bp.route('/favorites', methods=['GET'])
def list_favorites():
    user_id = request.args.get('user_id')  # У реальному додатку user_id береться з токена
    return get_favorites(user_id)

@recipes_bp.route('/filter', methods=['GET'])
def filter_recipes_api():
    filters = request.args.to_dict(flat=True)

    # Розділення інгредієнтів на список
    if 'ingredients' in filters:
        filters['ingredients'] = filters['ingredients'].split(',')

    return filter_recipes(filters)
