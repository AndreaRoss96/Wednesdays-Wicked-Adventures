from flask_login import UserMixin
from . import db

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True) 
    password = db.Column(db.String(100), nullable=False) 
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))
    bookings = db.relationship('Booking', backref='user')

    def get_id(self):
        return str(self.user_id)

    def to_json(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'role_id': self.role_id

        }

class Role(db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def to_json(self):
        return {
            'role_id': self.role_id,
            'name': self.name
        }
    
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