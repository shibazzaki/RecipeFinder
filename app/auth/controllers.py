from flask import Blueprint, request, jsonify
from .services import register_user, login_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
        Register a new user
        ---
        tags:
          - Authentication
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - email
                - password
              properties:
                email:
                  type: string
                  description: The user's email
                password:
                  type: string
                  description: The user's password
        responses:
          201:
            description: User registered successfully
          400:
            description: User already exists
        """
    data = request.get_json()
    return register_user(data)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
        Login a user
        ---
        tags:
          - Authentication
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - email
                - password
              properties:
                email:
                  type: string
                  description: The user's email
                password:
                  type: string
                  description: The user's password
        responses:
          200:
            description: Access token
          401:
            description: Invalid credentials
        """
    data = request.get_json()
    return login_user(data)
