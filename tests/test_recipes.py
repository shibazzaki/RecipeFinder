def test_add_recipe(client):
    response = client.post('/recipes/', json={
        "title": "Pancakes",
        "description": "Simple pancake recipe",
        "steps": "Mix ingredients. Cook on skillet.",
        "time_to_cook": 15,
        "servings": 4,
        "ingredients": ["flour", "milk", "egg"]
    })
    assert response.status_code == 201
    assert response.json["message"] == "Recipe created successfully"

def test_filter_recipes(client):
    # Додаємо рецепт
    client.post('/recipes/', json={
        "title": "Pancakes",
        "description": "Simple pancake recipe",
        "steps": "Mix ingredients. Cook on skillet.",
        "time_to_cook": 15,
        "servings": 4,
        "ingredients": ["flour", "milk", "egg"]
    })

    # Фільтруємо за інгредієнтами
    response = client.get('/recipes/filter?ingredients=flour,milk')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["title"] == "Pancakes"
