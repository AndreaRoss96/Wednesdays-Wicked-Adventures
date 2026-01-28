import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///flask_app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL", "sqlite:///flask_app.db")
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-fallback-key'

    @staticmethod
    def init_app(app):
        from app import db
        from app import models
        with app.app_context():
            db.drop_all()
            db.create_all()
            from app.seed_data.data import seed_dev_data
            seed_dev_data()

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")
    WTF_CSRF_ENABLED = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test-fallback-key'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URL")
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or None

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        if not cls.SECRET_KEY:
            raise RuntimeError("CRITICAL: SECRET_KEY environment variable must be set in production!")
        app.config['SECRET_KEY'] = cls.SECRET_KEY

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}