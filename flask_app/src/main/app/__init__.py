from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

## to enforce FK in SQLite3
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3

db = SQLAlchemy()

def create_app(config_name="development"):
    app = Flask(__name__)
    ## Login ## 
    app.config['SECRET_KEY'] = 'secret-key'
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    ## Enforce FK in SQLite3 ##
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        if isinstance(dbapi_connection, sqlite3.Connection):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.close()

    db.init_app(app)

    # create db locally and seed data (roles and parks) 
    if config_name == "development":
        from app import models
        with app.app_context():
            db.drop_all()
            db.create_all()

            from app.seed_data.data import seed_dev_data
            seed_dev_data()


    # Configure Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'login.login'
    login_manager.init_app(app)
    
    # User loader function for Flask-Login
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register Blueprints
    ## UI Routes
    from .login import auth_login as login_blueprint
    app.register_blueprint(login_blueprint)   
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    return app