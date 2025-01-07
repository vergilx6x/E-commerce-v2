##!/usr/bin/python3
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")  # General secret
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_jwt_secret")  # J
    DEBUG = os.getenv('DEBUG')

