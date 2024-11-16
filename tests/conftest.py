import pytest
from app import create_app
from app.extensions import db
from app.auth.models import User

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"  # Тестова БД в пам'яті
    })

    with app.app_context():
        db.create_all()

        # Додати тестового користувача
        test_user = User(email="test@example.com", password_hash="hashed_password")
        db.session.add(test_user)
        db.session.commit()

        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
