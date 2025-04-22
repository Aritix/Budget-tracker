from flask import Flask
from src.backend.api import api

def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(api)
    app.config['environment'] = 'unit testing'
    return app