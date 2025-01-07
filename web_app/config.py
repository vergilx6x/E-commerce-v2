import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback_secret_key')  # Default secret key for sessions
    DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']  # Convert to bool
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///default.db')  # Default to SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # To suppress warnings
