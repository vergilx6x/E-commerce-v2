import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback_secret_key')
    DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # To suppress warnings
