from decouple import config
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

from db import db
from endpoints.routes import routes


class EnvironmentConfig:
    FLASK_ENV = config("ENVIRONMENT")
    DEBUG = config("ENVIRONMENT_DEBUG")
    TESTING = config("ENVIRONMENT_TESTING")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('DB_NAME')}"
    )


class TestingConfig:
    """Configurations for Testing, with a separate test database."""

    DEBUG = config("TEST_ENVIRONMENT_DEBUG")
    TESTING = config("TEST_ENVIRONMENT_TESTING")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('TEST_DB_NAME')}"
    )


def create_app(config="config.EnvironmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config)

    api = Api(app)
    migrate = Migrate(app, db)
    CORS(app)
    [api.add_resource(*route) for route in routes]
    return app
