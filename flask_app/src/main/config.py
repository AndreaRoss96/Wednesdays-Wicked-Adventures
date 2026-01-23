import os

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///flask_app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WTF_CSRF_ENABLED = True 
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hour

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL", "sqlite:///flask_app.db")
    SECRET_KEY = 'dev-secret-key'

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
    SECRET_KEY = 'test-secret-key'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URL")
    WTF_CSRF_ENABLED = True   
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise RuntimeError("CRITICAL: SECRET_KEY environment variable must be set in production!")
    
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}