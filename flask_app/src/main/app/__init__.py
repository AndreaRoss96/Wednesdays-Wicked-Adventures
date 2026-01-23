from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_wtf.csrf import CSRFProtect
import os
from config import config

## to enforce FK in SQLite3
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3

db = SQLAlchemy()
csrf = CSRFProtect()

 ## Enforce FK in SQLite3 ##
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

def create_app(config_name="development"): 

    basedir = os.path.abspath(os.path.dirname(__file__))

    #app = Flask(__name__)
    app = Flask(__name__,
                template_folder=os.path.join(basedir, 'templates'),
                static_folder=os.path.join(basedir, 'static'))
    app.config.from_object(config[config_name])
    db.init_app(app)
    csrf.init_app(app)
    config[config_name].init_app(app)

    from .models import User, Role, Booking, Park, Message, AppIndexView, UserView, RoleView, BookingView, ParkView, MessageView
    
    # Configure Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'login.login'
    login_manager.init_app(app)
    
    # User loader function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    
    # Flask-Admin
    admin = Admin (app, name='Wednesdays-Wicked-Adventures', template_mode='bootstrap4', index_view=AppIndexView())
    admin.add_view(UserView(User, db.session))
    admin.add_view(RoleView(Role, db.session))
    admin.add_view(BookingView(Booking, db.session))
    admin.add_view(ParkView(Park, db.session))
    admin.add_view(MessageView(Message, db.session))
    
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

