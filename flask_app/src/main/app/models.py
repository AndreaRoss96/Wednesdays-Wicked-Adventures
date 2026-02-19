from wtforms.validators import DataRequired, Email 
from werkzeug.security import generate_password_hash
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask import redirect, url_for, flash
from . import db

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False) 
    password = db.Column(db.String(255), nullable=False) 
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))
    bookings = db.relationship('Booking', backref='user')
    role = db.relationship('Role', back_populates='users')

    def get_id(self):
        return str(self.user_id)
    
    def has_role(self, role_name: str) -> bool:
        return (
            self.role is not None and
            self.role.name == role_name
        )
    
    def to_json(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'role_id': self.role_id

        }
     
    def __str__(self):
        return self.name + ' ' + self.last_name
    

class Role(db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', back_populates='role')

    def to_json(self):
        return {
            'role_id': self.role_id,
            'name': self.name
        }
    
    def __str__(self):
        return self.name
    
class Park(db.Model):
    __tablename__ = 'parks'
    park_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(200), default='images/parks/default.jpg')
    short_description = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    folder = db.Column(db.String(50), default='')
    hours = db.Column(db.String(100), default='9:00 AM - 10:00 PM')
    difficulty = db.Column(db.String(50), default='Moderate')
    min_age = db.Column(db.Integer, default=12)
    price = db.Column(db.String(50), default='Starting at $49.99')
    wait_time = db.Column(db.String(50), default='30-60 minutes')
    height_requirement = db.Column(db.String(50), default='48" (1.2m)')
    bookings = db.relationship('Booking', backref='park')
    

    def to_json(self):
        return {
            'park_id': self.park_id,
            'name': self.name,
            'location': self.location,
            'description': self.description,
            'image_path': self.image_path,
            'short_description': self.short_description,
            'slug': self.slug,
            'folder': self.folder,
            'hours': self.hours, 
            'difficulty':self.difficulty,
            'min_age': self.min_age,
            'price':self.price, 
            'wait_time': self.wait_time,
            'height_requirement': self.height_requirement
 
        }

    def __str__(self):
        return self.name
    

class Booking(db.Model):
    __tablename__ = 'bookings'
    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    park_id = db.Column(db.Integer, db.ForeignKey('parks.park_id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    num_tickets = db.Column(db.Integer, nullable=False, default=1)
    health_safety = db.Column(db.Boolean, nullable=False, default=False)

    def to_json(self):
        return {
            'booking_id': self.booking_id,
            'user_id': self.user_id,
            'park_id': self.park_id,
            'date': self.date.isoformat(),
            'num_tickets': self.num_tickets,
            'health_safety':self.health_safety
        }
    
    def __repr__(self):
        return f''
    
class Message(db.Model):
    __tablename__ = 'messages'
    message_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def to_json(self):
        return {
            'message_id': self.message_id,
            'name': self.name,
            'email': self.email,
            'message': self.message,
            'created_at': self.created_at.isoformat()
        }


class AppModelView(ModelView):
    def is_accessible(self):
        return (current_user.is_authenticated and current_user.has_role('admin'))
    
    def inaccessible_callback(self, name, **kwargs):
        flash('ADMIN ACCESS ONLY! Please login with Admin credentials!')
        return redirect(url_for("login.login"))

class AppIndexView(AdminIndexView):
    def is_accessible(self):
        return (current_user.is_authenticated and current_user.has_role('admin'))
    
    def inaccessible_callback(self, name, **kwargs):
        flash('ADMIN ACCESS ONLY! Please login with Admin credentials!')
        return redirect(url_for("login.login"))
    

class UserView(AppModelView):

    column_list = ('name', 'last_name', 'email', 'password', 'role') 
    column_labels = {
        'name': 'Name',
        'last_name': 'Last Name',
        'email': 'Email',
        'password': 'Password',
        'role': 'Role'
    }  # nosec  
    column_filters = ('name', 'email')
    column_formatters = {
        'password': lambda v, c, m, p: '*****'
    }
    column_searchable_list = ('name', 'email')
    column_sortable_list = ()
    form_columns = ('name', 'last_name', 'email', 'password', 'role')
    form_args = {
        'name': {'validators': [DataRequired()]},
        'last_name': {'validators': [DataRequired()]},
        'email': {'validators': [DataRequired()]},
        'password': {'validators': [DataRequired()]},
        'role': {'validators': [DataRequired()]}
    }

    def on_model_change(self, form, model, is_created):
        model.password = generate_password_hash(model.password, method='pbkdf2:sha256')

class RoleView(AppModelView):

    column_list = ('name',)
    column_labels = {
        'name': 'Name'
    }
    column_filters = ('name',)
    column_searchable_list = ('name',)
    column_sortable_list = () 
    form_columns = ('name',)
    form_args = {
        'name': {'validators': [DataRequired()]}
    }

class BookingView(AppModelView):
  
    column_list = ('park', 'date', 'num_tickets', 'health_safety', 'user')  
    column_labels = {
        'park': 'Park',
        'date': 'Date',
        'num_tickets': 'Number of Tickets',
        'health_safety': 'Health & Safety',
        'user': 'User'
    }  
    column_filters = ('park', 'user')
    column_searchable_list = ('park.name', 'user.name')
    column_sortable_list = ()  
    form_columns = ('park', 'date', 'num_tickets', 'health_safety', 'user') 
    form_args = {
        'park': {'validators': [DataRequired()]},
        'user': {'validators': [DataRequired()]},
        'date': {'validators': [DataRequired()]},
        'num_tickets': {'validators': [DataRequired()]},
        'health_safety': {'validators': [DataRequired()]}
    }

class ParkView(AppModelView):
  
    column_list = ('name', 'location', 'description', 'image_path', 'short_description', 'slug', 'folder', 'hours', 'min_age', 'price', 'wait_time', 'height_requirement')
    column_labels = {
        'name': 'Name',
        'location': 'Location',
        'description': 'Description',
        'image_path': 'Image Path',
        'short_description': 'Short Description',
        'slug': 'Slug',
        'folder': 'Folder',
        'hours': 'Hours',
        'min_age': 'Min Age',
        'price': 'Price',
        'wait_time': 'Wait Time',
        'height_requirement': 'Height Requirement'
    }
    column_filters = ('name', 'location')
    column_formatters = {
        'description': lambda v, c, m, p: m.description[:50] + '...'
    }
    column_searchable_list = ('name', 'location')
    column_sortable_list = ()
    form_columns = ('name', 'location', 'description', 'image_path', 'short_description', 'slug', 'folder', 'hours', 'min_age', 'price', 'wait_time', 'height_requirement')
    form_args = {
        'name': {'validators': [DataRequired()]},
        'location': {'validators': [DataRequired()]},
        'description': {'validators': [DataRequired()]},
        'image_path': {'validators': [DataRequired()]},
        'short_description': {'validators': [DataRequired()]},
        'slug': {'validators': [DataRequired()]},
        'folder': {'validators': [DataRequired()]},
        'hours': {'validators': [DataRequired()]},
        'min_age': {'validators': [DataRequired()]},
        'price': {'validators': [DataRequired()]},
        'wait_time': {'validators': [DataRequired()]},
        'height_requirement': {'validators': [DataRequired()]}
    }

class MessageView(AppModelView):
   
    column_list = ('name', 'email', 'message', 'created_at')
    column_labels = {'name': 'Name', 'email': 'Email', 'message': 'Message', 'created_at': 'Create Date'}
    column_filters = ('email',)
    column_searchable_list = ('name', 'email', 'message')
    column_sortable_list = ()
    column_default_sort = ('created_at', True)
    form_columns = ('name', 'email', 'message', 'created_at')
    form_args = {
        'name': {'validators': [DataRequired()]},
        'email': {'validators': [DataRequired()]},
        'message': {'validators': [DataRequired()]}
    }

