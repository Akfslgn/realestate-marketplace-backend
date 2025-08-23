from os import getenv

from dotenv import load_dotenv

load_dotenv(".env")


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APISPEC_SWAGGER_UI_URL = "/docs"
    APISPEC_TITLE = "Kickstart API"
    APISPEC_VERSION = "1.0.0"
    SECRET_KEY = getenv("SECRET_KEY")
    CLOUDINARY_CLOUD_NAME = getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = getenv("CLOUDINARY_API_SECRET")
    OPENAI_API_KEY = getenv("OPENAI_API_KEY")
    
    # CORS Configuration
    CORS_ORIGINS = getenv("CORS_ORIGINS", "*").split(",") if getenv("CORS_ORIGINS") else ["*"]


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite+pysqlite:///:memory:"
    TESTING = True


class ProductionConfig(BaseConfig):
    DEBUG = False


def get_config(env):
    return {
        "development": DevelopmentConfig,
        "testing": TestConfig,
        "production": ProductionConfig,
    }.get(env or getenv("FLASK_ENV", "development"))
