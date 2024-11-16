import unittest
from app import create_app
from app.extensions import db
from app.auth.models import User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register(self):
        response = self.client.post('/auth/register', json={
            "email": "test@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("User registered successfully", response.json['message'])

    def test_login(self):
        with self.app.app_context():
            user = User(email="test@example.com", password_hash="hashed_password")
            db.session.add(user)
            db.session.commit()

        response = self.client.post('/auth/login', json={
            "email": "test@example.com",
            "password": "hashed_password"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json)

if __name__ == '__main__':
    unittest.main()
