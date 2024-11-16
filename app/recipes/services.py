from app.extensions import db
from app.recipes.models import Recipe, RecipeIngredient, Ingredient

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
            ingredient = Ingredient(name=ingredient_name)
            db.session.add(ingredient)
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
