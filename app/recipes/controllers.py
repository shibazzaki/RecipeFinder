from flask import Blueprint, request, jsonify, session, redirect, flash, url_for
from app.recipes.services import create_recipe, get_recipes, delete_recipe, add_to_favorites, remove_from_favorites, \
    get_favorites, filter_recipes, get_random_recipe

from app.recipes.services import mark_recipe_as_tried
recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('/', methods=['POST'])
def add_recipe():
    """
        Add a new recipe
        ---
        tags:
          - Recipes
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - title
                - steps
                - time_to_cook
                - servings
              properties:
                title:
                  type: string
                  description: The recipe title
                description:
                  type: string
                  description: A short description of the recipe
                steps:
                  type: string
                  description: Steps to prepare the recipe
                time_to_cook:
                  type: integer
                  description: Time in minutes
                servings:
                  type: integer
                  description: Number of servings
                ingredients:
                  type: array
                  items:
                    type: string
                  description: List of ingredient names
        responses:
          201:
            description: Recipe created successfully
          400:
            description: Bad request
        """
    data = request.get_json()
    return create_recipe(data)

@recipes_bp.route('/', methods=['GET'])
def list_recipes():
    """
        List all recipes
        ---
        tags:
          - Recipes
        responses:
          200:
            description: A list of all recipes
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: Recipe ID
                  title:
                    type: string
                    description: Recipe title
                  description:
                    type: string
                    description: Recipe description
                  time_to_cook:
                    type: integer
                    description: Time to cook in minutes
                  servings:
                    type: integer
                    description: Number of servings
        """
    return get_recipes()

@recipes_bp.route('/<int:recipe_id>', methods=['DELETE'])
def remove_recipe(recipe_id):
    """
       Delete a recipe by ID
       ---
       tags:
         - Recipes
       parameters:
         - name: recipe_id
           in: path
           required: true
           type: integer
           description: ID of the recipe to delete
       responses:
         200:
           description: Recipe deleted successfully
         404:
           description: Recipe not found
       """
    return delete_recipe(recipe_id)

@recipes_bp.route('/favorites', methods=['POST'])
def add_favorite():
    """
    Add a recipe to favorites
    ---
    tags:
      - Favorites
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - recipe_id
          properties:
            recipe_id:
              type: integer
              description: Recipe ID
    responses:
      201:
        description: Recipe added to favorites
      400:
        description: Recipe is already in favorites
      404:
        description: Recipe not found
    """
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()
    recipe_id = data.get('recipe_id')
    user_id = session['user_id']

    response, status = add_to_favorites(user_id, recipe_id)
    return jsonify(response), status


@recipes_bp.route('/favorites/<int:recipe_id>', methods=['DELETE'])
def remove_favorite(recipe_id):
    """
       Remove a recipe from favorites
       ---
       tags:
         - Favorites
       parameters:
         - name: recipe_id
           in: path
           required: true
           type: integer
           description: ID of the recipe to remove from favorites
         - name: user_id
           in: query
           required: true
           type: integer
           description: ID of the user
       responses:
         200:
           description: Recipe removed from favorites
         404:
           description: Recipe not found in favorites
       """
    user_id = request.args.get('user_id')  # У реальному додатку user_id береться з токена
    return remove_from_favorites(user_id, recipe_id)

@recipes_bp.route('/favorites', methods=['GET'])
def list_favorites():
    """
        List favorite recipes for a user
        ---
        tags:
          - Favorites
        parameters:
          - name: user_id
            in: query
            required: true
            type: integer
            description: ID of the user
        responses:
          200:
            description: A list of favorite recipes
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: Recipe ID
                  title:
                    type: string
                    description: Recipe title
                  description:
                    type: string
                    description: Recipe description
                  time_to_cook:
                    type: integer
                    description: Time to cook in minutes
                  servings:
                    type: integer
                    description: Number of servings
        """
    user_id = request.args.get('user_id')  # У реальному додатку user_id береться з токена
    return get_favorites(user_id)

@recipes_bp.route('/filter', methods=['GET'])
def filter_recipes_api():
    """
        Filter recipes
        ---
        tags:
          - Recipes
        parameters:
          - name: ingredients
            in: query
            type: string
            description: Comma-separated list of ingredients
          - name: max_time
            in: query
            type: integer
            description: Maximum cooking time in minutes
          - name: search
            in: query
            type: string
            description: Search term for recipe title or description
        responses:
          200:
            description: List of filtered recipes
        """
    filters = request.args.to_dict(flat=True)

    # Розділення інгредієнтів на список
    if 'ingredients' in filters:
        filters['ingredients'] = filters['ingredients'].split(',')

    return filter_recipes(filters)



@recipes_bp.route('/tried/<int:recipe_id>', methods=['POST'])
def mark_as_tried(recipe_id):
    """
    Mark a recipe as tried
    ---
    tags:
      - Recipes
    parameters:
      - name: recipe_id
        in: path
        required: true
        type: integer
        description: ID of the recipe to mark as tried
      - name: Authorization
        in: header
        required: true
        type: string
        description: Bearer token for user authentication
    responses:
      200:
        description: Recipe successfully marked as tried
      400:
        description: Recipe already marked as tried
      401:
        description: Unauthorized user
      404:
        description: Recipe not found
    """
    if 'user_id' not in session:
        if request.is_json:  # If API request
            return jsonify({"message": "Unauthorized"}), 401
        else:  # If request is from Web UI
            flash('You need to log in to perform this action.', 'danger')
            return redirect(url_for('recipes.list_recipes'))

    user_id = session['user_id']
    response, status = mark_recipe_as_tried(user_id, recipe_id)

    # If request is API
    if request.is_json:
        return jsonify(response), status

    # If request is from Web UI
    if status == 200:
        flash('Recipe marked as tried!', 'success')
    else:
        flash(response.get('message', 'An error occurred.'), 'danger')
    return redirect(url_for('recipes.list_recipes'))

@recipes_bp.route('/random', methods=['GET'])
def random_recipe():
    """
    Get a random recipe
    ---
    tags:
      - Recipes
    responses:
      200:
        description: A random recipe
        schema:
          type: object
          properties:
            id:
              type: integer
              description: Recipe ID
            title:
              type: string
              description: Recipe title
            description:
              type: string
              description: Recipe description
            time_to_cook:
              type: integer
              description: Time to cook in minutes
            servings:
              type: integer
              description: Number of servings
      404:
        description: No recipes found
    """
    response, status = get_random_recipe()
    return jsonify(response), status