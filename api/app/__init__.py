# api/app/__init__.py

from flask import Flask
from api.app.config import Config

app = Flask(__name__)
app.config.from_object(Config)  # Load config from the Config class

# Optionally, set other configurations for different environments
