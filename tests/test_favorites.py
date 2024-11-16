def test_add_to_favorites(client):
    # Додаємо рецепт
    client.post('/recipes/', json={
        "title": "Pancakes",
        "description": "Simple pancake recipe",
        "steps": "Mix ingredients. Cook on skillet.",
        "time_to_cook": 15,
        "servings": 4,
        "ingredients": ["flour", "milk", "egg"]
    })

    # Додаємо до улюблених
    response = client.post('/recipes/favorites', json={
        "user_id": 1,  # ID тестового користувача
        "recipe_id": 1
    })
    assert response.status_code == 201
    assert response.json["message"] == "Recipe added to favorites"

