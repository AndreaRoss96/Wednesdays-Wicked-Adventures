"""
Unit tests for database models
"""
import pytest
import sys
import os

# Add the main directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'main'))

from app.models import User, Role, Park, Booking, Message
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from unittest.mock import patch, MagicMock
from app.models import AppModelView, AppIndexView, UserView, User, Role, Park
from app import db

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
    
    def test_user_has_role(self, app):
        """Test User.has_role() method"""
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            admin = User.query.filter_by(email='admin@example.com').first()
            
            assert user.has_role('user') == True
            assert user.has_role('admin') == False
            assert admin.has_role('admin') == True
            assert admin.has_role('user') == False
        
    def test_user_str_representation(self, app):
        """Test User.__str__() method"""
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            assert str(user) == 'Test User'

    def test_user_to_json(self, app):
        """Test User.to_json() method"""
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            json_data = user.to_json()
            assert 'user_id' in json_data
            assert 'name' in json_data
            assert 'email' in json_data
            assert json_data['email'] == 'test@example.com'

    def test_user_password_not_stored_plain(self, app):
        """Test that passwords are hashed"""
        with app.app_context():
            from app import db
            
            # Create a fresh user for this test
            customer_role = Role.query.filter_by(name='user').first()
            test_password = 'freshpass123'
            fresh_user = User(
                name='Fresh',
                last_name='Test',
                email='fresh@test.com',
                password=generate_password_hash(test_password, method='pbkdf2:sha256'),
                role_id=customer_role.role_id
            )
            db.session.add(fresh_user)
            db.session.commit()
            
            # Verify password is hashed
            assert fresh_user.password != test_password
            assert check_password_hash(fresh_user.password, test_password)

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
    
    def test_role_str_representation(self, app):
        """Test Role.__str__() method"""
        with app.app_context():
            role = Role.query.filter_by(name='user').first()
            assert str(role) == 'user'

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
            assert park.location == 'Test City'
            assert park.slug == 'test-park'
            assert park.difficulty == 'Easy'
            assert park.min_age == 5

    def test_park_to_json_includes_new_fields(self, app):
        """Test Park.to_json() includes all new fields"""
        with app.app_context():
            park = Park.query.first()
            json_data = park.to_json()
            
            assert 'park_id' in json_data
            assert 'name' in json_data
            assert 'location' in json_data
            assert 'description' in json_data
            assert 'image_path' in json_data
            assert 'short_description' in json_data
            assert 'slug' in json_data
            assert 'folder' in json_data
            assert 'hours' in json_data
            assert 'difficulty' in json_data
            assert 'min_age' in json_data
            assert 'price' in json_data
            assert 'wait_time' in json_data
            assert 'height_requirement' in json_data

    def test_park_slug_unique(self, app):
        """Test that park slug must be unique"""
        with app.app_context():
            from app import db
            
            park1 = Park(
                name='Park A',
                location='Location A',
                description='Description A',
                short_description='Short A',
                slug='unique-slug'
            )
            db.session.add(park1)
            db.session.commit()
            
            park2 = Park(
                name='Park B',
                location='Location B',
                description='Description B',
                short_description='Short B',
                slug='unique-slug'
            )
            db.session.add(park2)
            with pytest.raises(Exception):
                db.session.commit()
            db.session.rollback()

    def test_park_str_representation(self, app):
        """Test Park.__str__() method"""
        with app.app_context():
            park = Park.query.first()
            assert str(park) == park.name

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
    
    def test_park_default_values(self, app):
        """Test park default values"""
        with app.app_context():
            from app import db
            
            park = Park(
                name='Minimal Park',
                location='Somewhere',
                description='Basic',
                short_description='Short',
                slug='minimal-park'
            )
            db.session.add(park)
            db.session.commit()
            
            assert park.image_path == 'images/parks/default.jpg'
            assert park.folder == ''
            assert park.hours == '9:00 AM - 10:00 PM'
            assert park.difficulty == 'Moderate'
            assert park.min_age == 12
            assert park.price == 'Starting at $49.99'
            assert park.wait_time == '30-60 minutes'
            assert park.height_requirement == '48" (1.2m)'

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

class TestMessageModel:
    """Test Message model"""
    
    def test_message_creation(self, app):
        """Test creating a message"""
        with app.app_context():
            from app import db
            
            message = Message(
                name='John Doe',
                email='john@example.com',
                message='This is a test message'
            )
            db.session.add(message)
            db.session.commit()
            
            assert message.name == 'John Doe'
            assert message.email == 'john@example.com'
            assert message.message == 'This is a test message'
            assert message.created_at is not None
    
    def test_message_to_json(self, app):
        """Test Message.to_json() method"""
        with app.app_context():
            from app import db
            
            message = Message(
                name='Test User',
                email='test@example.com',
                message='Test message content'
            )
            db.session.add(message)
            db.session.commit()
            
            json_data = message.to_json()
            assert 'message_id' in json_data
            assert 'name' in json_data
            assert 'email' in json_data
            assert 'message' in json_data
            assert 'created_at' in json_data

class TestAppModelView:
    
    def test_is_accessible_admin(self, app):
        """ test is_accessible function"""
        with app.app_context():
            view = AppModelView(User, None)
            with patch('app.models.current_user') as mock_user:
                mock_user.is_authenticated = True
                mock_user.has_role = MagicMock(return_value=True)
                result = view.is_accessible()
                assert result == True
    
    def test_is_accessible_not_admin(self, app):
        """test is_accessible returns False for non-admin"""
        with app.app_context():
            view = AppModelView(User, None)
            with patch('app.models.current_user') as mock_user:
                mock_user.is_authenticated = True
                mock_user.has_role = MagicMock(return_value=False)
                result = view.is_accessible()
                assert result == False
    
    def test_inaccessible_callback(self, app):
        """test inaccessible_callback flashes and redirects"""
        with app.app_context():
            view = AppModelView(User, None)
            with patch('app.models.flash') as mock_flash:
                with patch('app.models.redirect') as mock_redirect:
                    with patch('app.models.url_for') as mock_url_for:
                        mock_redirect.return_value = MagicMock()
                        view.inaccessible_callback('test')
                        
                        mock_flash.assert_called_once()
                        mock_url_for.assert_called_once_with("login.login")
                        mock_redirect.assert_called_once()

class TestAppIndexView:
    """Test AppIndexView"""
    
    def test_is_accessible_admin(self, app):
        """is_accessible returns True for admin"""
        with app.app_context():
            view = AppIndexView()
            with patch('app.models.current_user') as mock_user:
                mock_user.is_authenticated = True
                mock_user.has_role = MagicMock(return_value=True)
                result = view.is_accessible()
                assert result == True
    
    def test_is_accessible_not_admin(self, app):
        """is_accessible returns False for non-admin"""
        with app.app_context():
            view = AppIndexView()
            with patch('app.models.current_user') as mock_user:
                mock_user.is_authenticated = False
                mock_user.has_role = MagicMock(return_value=False)
                result = view.is_accessible()
                assert result == False
    
    def test_inaccessible_callback(self, app):
        """inaccessible_callback flashes and redirects"""
        with app.app_context():
            view = AppIndexView()
            with patch('app.models.flash') as mock_flash:
                with patch('app.models.redirect') as mock_redirect:
                    with patch('app.models.url_for') as mock_url_for:
                        mock_redirect.return_value = MagicMock()
                        view.inaccessible_callback('test')
                        
                        mock_flash.assert_called_once()
                        mock_url_for.assert_called_once_with("login.login")
                        mock_redirect.assert_called_once()


class TestUserView:
    """Test UserView"""
    
    def test_on_model_change_hashes_password(self, app):
        """on_model_change hashes password"""
        with app.app_context():
            # Create a role first (check if exists)
            role = Role.query.filter_by(name='user').first()
            if not role:
                role = Role(name='user')
                db.session.add(role)
                db.session.commit()
            
            view = UserView(User, None)
            form = MagicMock()
            
            user = User(
                name='Test',
                last_name='User',
                email='test@test.com',
                password=generate_password_hash('pass', method='pbkdf2:sha256'),
                role_id=role.role_id
            )
            
            # Change password before calling on_model_change (simulating form submission)
            new_password = 'newpass'
            user.password = new_password
            
            view.on_model_change(form, user, is_created=False)
            
            # Password should be hashed after on_model_change
            assert user.password != 'newpass'
            assert check_password_hash(user.password, 'newpass')