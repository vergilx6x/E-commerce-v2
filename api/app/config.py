##!/usr/bin/python3
import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_jwt_secret")  # J
    DEBUG = os.getenv('DEBUG')
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)  # Set
