import os
from dotenv import load_dotenv

# Завантаження змінних з .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///fallback.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER = {'title': 'Recipe Finder API', 'uiversion': 3}
    SCHEDULER_API_ENABLED = True
