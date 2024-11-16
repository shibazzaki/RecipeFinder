from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.auth.models import User

def register_user(data):
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return {"message": "User already exists"}, 400

    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return {"message": "User registered successfully"}, 201

def login_user(data):
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return {"message": "Invalid credentials"}, 401

    access_token = create_access_token(identity=user.id)
    return {"access_token": access_token}, 200
