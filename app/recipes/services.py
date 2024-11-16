from app.extensions import db
from app.recipes.models import Recipe, RecipeIngredient, Ingredient, FavoriteRecipe

def create_recipe(data):
    title = data.get('title')
    description = data.get('description')
    steps = data.get('steps')
    time_to_cook = data.get('time_to_cook')
    servings = data.get('servings')
    ingredients = data.get('ingredients')  # Список назв інгредієнтів

    # Створюємо рецепт
    new_recipe = Recipe(
        title=title,
        description=description,
        steps=steps,
        time_to_cook=time_to_cook,
        servings=servings
    )
    db.session.add(new_recipe)
    db.session.commit()

    # Додаємо інгредієнти до рецепта
    for ingredient_name in ingredients:
        ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
        if not ingredient:
            # Якщо інгредієнт не існує, створюємо новий
            ingredient = Ingredient(name=ingredient_name)
            db.session.add(ingredient)
            db.session.commit()  # Зберігаємо інгредієнт у базі, щоб отримати його ID
        recipe_ingredient = RecipeIngredient(recipe_id=new_recipe.id, ingredient_id=ingredient.id)
        db.session.add(recipe_ingredient)

    db.session.commit()
    return {"message": "Recipe created successfully"}, 201


def get_recipes():
    recipes = Recipe.query.all()
    result = []
    for recipe in recipes:
        result.append({
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "time_to_cook": recipe.time_to_cook,
            "servings": recipe.servings
        })
    return result, 200

def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return {"message": "Recipe not found"}, 404

    db.session.delete(recipe)
    db.session.commit()
    return {"message": "Recipe deleted successfully"}, 200

def add_to_favorites(user_id, recipe_id):
    # Перевірка, чи рецепт існує
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return {"message": "Recipe not found"}, 404

    # Перевірка, чи вже в улюблених
    if FavoriteRecipe.query.filter_by(user_id=user_id, recipe_id=recipe_id).first():
        return {"message": "Recipe is already in favorites"}, 400

    favorite = FavoriteRecipe(user_id=user_id, recipe_id=recipe_id)
    db.session.add(favorite)
    db.session.commit()
    return {"message": "Recipe added to favorites"}, 201

def remove_from_favorites(user_id, recipe_id):
    favorite = FavoriteRecipe.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if not favorite:
        return {"message": "Recipe not found in favorites"}, 404

    db.session.delete(favorite)
    db.session.commit()
    return {"message": "Recipe removed from favorites"}, 200

def get_favorites(user_id):
    favorites = FavoriteRecipe.query.filter_by(user_id=user_id).all()
    result = []
    for favorite in favorites:
        result.append({
            "id": favorite.recipe.id,
            "title": favorite.recipe.title,
            "description": favorite.recipe.description,
            "time_to_cook": favorite.recipe.time_to_cook,
            "servings": favorite.recipe.servings
        })
    return result, 200