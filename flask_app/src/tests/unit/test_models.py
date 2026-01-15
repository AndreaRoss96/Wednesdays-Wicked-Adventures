"""
Unit tests for database models
"""
import pytest
import sys
import os

# Add the main directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'main'))

from app.models import User, Role, Park, Booking
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class TestUserModel:
    """Test User model"""

    def test_user_creation(self, app):
        """Test creating a user"""
        with app.app_context():
            user = User(
                name='John',
                last_name='Doe',
                email='john@example.com',
                password=generate_password_hash('test123', method='pbkdf2:sha256'),
                role_id=1
            )
            # Verify user attributes
            assert user.name == 'John'
            assert user.last_name == 'Doe'
            assert user.email == 'john@example.com'
            assert check_password_hash(user.password, 'test123')

    def test_user_get_id(self, app):
        """Test User.get_id() method"""
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            assert user.get_id() == str(user.user_id)

    def test_user_to_json(self, app):
        """Test User.to_json() method"""
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            json_data = user.to_json()
            # JSON should include required fields
            assert 'user_id' in json_data
            assert 'name' in json_data
            assert 'email' in json_data
            assert json_data['email'] == 'test@example.com'

    def test_user_password_not_stored_plain(self, app):
        """Test that passwords are hashed"""
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            # Password should be hashed, not plaintext
            assert user.password != 'password123'
            assert check_password_hash(user.password, 'password123')

    def test_user_unique_email(self, app):
        """Test that email must be unique"""
        with app.app_context():
            from app import db
            user1 = User(
                name='User1',
                last_name='Test',
                email='unique@test.com',
                password=generate_password_hash('pass', method='pbkdf2:sha256'),
                role_id=1
            )
            db.session.add(user1)
            db.session.commit()

            # Duplicate email should raise an exception
            user2 = User(
                name='User2',
                last_name='Test',
                email='unique@test.com',
                password=generate_password_hash('pass', method='pbkdf2:sha256'),
                role_id=1
            )
            db.session.add(user2)
            with pytest.raises(Exception):
                db.session.commit()
            db.session.rollback()

    def test_user_relationship_with_bookings(self, app):
        """Test User-Booking relationship"""
        with app.app_context():
            from app import db
            user = User.query.filter_by(email='test@example.com').first()
            park = Park.query.first()

            booking = Booking(
                user_id=user.user_id,
                park_id=park.park_id,
                date=datetime(2026, 6, 15),
                num_tickets=2,
                health_safety=True
            )
            db.session.add(booking)
            db.session.commit()

            # User should have at least one booking
            db.session.refresh(user)
            assert len(user.bookings) > 0
            assert any(b.booking_id == booking.booking_id for b in user.bookings)

class TestRoleModel:
    """Test Role model"""

    def test_role_creation(self, app):
        """Test creating a role"""
        with app.app_context():
            from app import db
            role = Role(name='test_role')
            db.session.add(role)
            db.session.commit()
            # Role should be created with correct name and ID
            assert role.name == 'test_role'
            assert role.role_id is not None

    def test_role_to_json(self, app):
        """Test Role.to_json() method"""
        with app.app_context():
            role = Role.query.filter_by(name='user').first()
            json_data = role.to_json()
            # JSON should include required fields
            assert 'role_id' in json_data
            assert 'name' in json_data
            assert json_data['name'] == 'user'

    def test_role_user_relationship(self, app):
        """Test Role-User relationship"""
        with app.app_context():
            role = Role.query.filter_by(name='user').first()
            # Role should have at least one user
            assert len(role.users) > 0

class TestParkModel:
    """Test Park model"""

    def test_park_creation(self, app):
        """Test creating a park"""
        with app.app_context():
            park = Park(
                name='Test Park',
                location='Test City',
                description='A test park description',
                short_description='Short test desc',
                slug='test-park',
                image_path='images/test.png',
                folder='test',
                hours='9:00 AM - 6:00 PM',
                difficulty='Easy',
                min_age=5,
                price='$25.00',
                wait_time='10-20 minutes',
                height_requirement='36" (0.9m)'
            )
            # Park attributes should match
            assert park.name == 'Test Park'
            assert park.location == 'Test Location'

    def test_park_to_json(self, app):
        """Test Park.to_json() method"""
        with app.app_context():
            park = Park.query.first()
            json_data = park.to_json()
            # JSON should include required fields
            assert 'park_id' in json_data
            assert 'name' in json_data
            assert 'location' in json_data
            assert 'description' in json_data

    def test_park_booking_relationship(self, app):
        """Test Park-Booking relationship"""
        with app.app_context():
            from app import db
            park = Park.query.first()
            user = User.query.first()

            booking = Booking(
                user_id=user.user_id,
                park_id=park.park_id,
                date=datetime(2026, 7, 1),
                num_tickets=1,
                health_safety=False
            )
            db.session.add(booking)
            db.session.commit()

            # Park should have at least one booking
            db.session.refresh(park)
            assert len(park.bookings) > 0

class TestBookingModel:
    """Test Booking model"""

    def test_booking_creation(self, app):
        """Test creating a booking"""
        with app.app_context():
            from app import db
            user = User.query.first()
            park = Park.query.first()

            booking = Booking(
                user_id=user.user_id,
                park_id=park.park_id,
                date=datetime(2026, 6, 15),
                num_tickets=2,
                health_safety=True
            )
            db.session.add(booking)
            db.session.commit()
            # Booking attributes should match
            assert booking.num_tickets == 2
            assert booking.health_safety == True
            assert booking.user_id == user.user_id

    def test_booking_default_values(self, app):
        """Test booking default values"""
        with app.app_context():
            from app import db
            user = User.query.first()
            park = Park.query.first()

            booking = Booking(
                user_id=user.user_id,
                park_id=park.park_id,
                date=datetime(2026, 7, 20)
            )
            db.session.add(booking)
            db.session.commit()
            # Default values should be set
            assert booking.num_tickets == 1
            assert booking.health_safety == False

    def test_booking_to_json(self, app):
        """Test Booking.to_json() method"""
        with app.app_context():
            from app import db
            user = User.query.first()
            park = Park.query.first()

            booking = Booking(
                user_id=user.user_id,
                park_id=park.park_id,
                date=datetime(2026, 7, 20),
                num_tickets=3,
                health_safety=False
            )
            db.session.add(booking)
            db.session.commit()

            json_data = booking.to_json()
            # JSON should include required fields
            assert 'booking_id' in json_data
            assert 'user_id' in json_data
            assert 'park_id' in json_data
            assert json_data['num_tickets'] == 3
            assert 'date' in json_data

    def test_booking_foreign_key_constraints(self, app):
        """Test that foreign key constraints work"""
        with app.app_context():
            from app import db

            # Invalid user_id should raise an exception
            with pytest.raises(Exception):
                booking = Booking(
                    user_id=99999,  # Non-existent user
                    park_id=1,
                    date=datetime(2026, 8, 1),
                    num_tickets=1
                )
                db.session.add(booking)
                db.session.commit()
            db.session.rollback()
