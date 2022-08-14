from decouple import config


class EnvironmentConfig:
    FLASK_ENV = config("ENVIRONMENT")
    DEBUG = config("ENVIRONMENT_DEBUG")
    TESTING = config("ENVIRONMENT_TESTING")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('DB_NAME')}"
    )
