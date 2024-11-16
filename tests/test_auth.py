def test_register(client):
    response = client.post('/auth/register', json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert response.json["message"] == "User registered successfully"

def test_login(client):
    # Реєструємо користувача
    client.post('/auth/register', json={
        "email": "test@example.com",
        "password": "password123"
    })

    # Логін
    response = client.post('/auth/login', json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json
