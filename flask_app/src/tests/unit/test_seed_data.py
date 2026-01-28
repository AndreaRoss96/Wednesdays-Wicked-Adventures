"""
Unit tests for seed data functionality
"""
import pytest
import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'main'))

from app.models import User, Role, Park
from app.seed_data.data import seed_dev_data
from werkzeug.security import check_password_hash, generate_password_hash


class TestSeedData:
    """Test seed_data.data module"""
    
    def test_seed_dev_data_creates_roles(self, app):
        """Test that seed_dev_data creates admin and customer roles"""
        with app.app_context():
            from app import db
            
            # Clear existing data
            User.query.delete()
            Park.query.delete()
            Role.query.delete()
            db.session.commit()
            
            # Set environment variable for password
            with patch.dict(os.environ, {'SEED_ADMIN_PASSWORD': 'test_admin_pass'}):
                seed_dev_data()
            
            # Verify roles created
            roles = Role.query.all()
            assert len(roles) == 2
            
            role_names = [role.name for role in roles]
            assert 'admin' in role_names
            assert 'customer' in role_names
    
    def test_seed_dev_data_creates_admin_users(self, app):
        """Test that seed_dev_data creates 2 admin users"""
        with app.app_context():
            from app import db
            
            # Clear existing data
            User.query.delete()
            Park.query.delete()
            Role.query.delete()
            db.session.commit()
            
            # Set environment variable
            test_password = 'secure_admin_password_123'
            with patch.dict(os.environ, {'SEED_ADMIN_PASSWORD': test_password}):
                seed_dev_data()
            
            # Verify admin users created
            admin_role = Role.query.filter_by(name='admin').first()
            admin_users = User.query.filter_by(role_id=admin_role.role_id).all()
            
            assert len(admin_users) == 2
            assert admin_users[0].email == 'admin1@example.com'
            assert admin_users[1].email == 'admin2@example.com'
            
            # Verify passwords are hashed correctly
            assert check_password_hash(admin_users[0].password, test_password)
            assert check_password_hash(admin_users[1].password, test_password)
    
    def test_seed_dev_data_creates_three_parks(self, app):
        """Test that seed_dev_data creates exactly 3 parks"""
        with app.app_context():
            from app import db
            
            # Clear existing data
            User.query.delete()
            Park.query.delete()
            Role.query.delete()
            db.session.commit()
            
            with patch.dict(os.environ, {'SEED_ADMIN_PASSWORD': 'test_pass'}):
                seed_dev_data()
            
            # Verify parks created
            parks = Park.query.all()
            assert len(parks) == 3
            
            park_names = [park.name for park in parks]
            assert "Witches' Park" in park_names
            assert "Spider Park" in park_names
            assert "Haunted House" in park_names
    
    def test_seed_dev_data_park_details(self, app):
        """Test that parks have all required fields populated"""
        with app.app_context():
            from app import db
            
            # Clear existing data
            User.query.delete()
            Park.query.delete()
            Role.query.delete()
            db.session.commit()
            
            with patch.dict(os.environ, {'SEED_ADMIN_PASSWORD': 'test_pass'}):
                seed_dev_data()
            
            # Check Witches' Park
            witches_park = Park.query.filter_by(name="Witches' Park").first()
            assert witches_park is not None
            assert witches_park.location == 'Dublin'
            assert witches_park.slug == 'park-1-dublin'
            assert witches_park.difficulty == 'Moderate'
            assert witches_park.min_age == 10
            assert witches_park.hours == '10:00 AM - 8:00 PM'
            assert witches_park.price == 'Starting at $39.99'
            
            # Check Spider Park
            spider_park = Park.query.filter_by(name='Spider Park').first()
            assert spider_park is not None
            assert spider_park.location == 'London'
            assert spider_park.difficulty == 'Hard'
            assert spider_park.min_age == 14
            
            # Check Haunted House
            haunted_park = Park.query.filter_by(name='Haunted House').first()
            assert haunted_park is not None
            assert haunted_park.location == 'Berlin'
            assert haunted_park.difficulty == 'Easy'
            assert haunted_park.min_age == 8
    
    def test_seed_dev_data_prevents_duplicate_seeding(self, app):
        """Test that seed_dev_data doesn't create duplicates if called twice"""
        with app.app_context():
            from app import db
            
            # Clear existing data
            User.query.delete()
            Park.query.delete()
            Role.query.delete()
            db.session.commit()
            
            with patch.dict(os.environ, {'SEED_ADMIN_PASSWORD': 'test_pass'}):
                # First seeding
                seed_dev_data()
                
                initial_role_count = Role.query.count()
                initial_park_count = Park.query.count()
                initial_user_count = User.query.count()
                
                # Second seeding (should do nothing)
                seed_dev_data()
                
                # Counts should remain the same
                assert Role.query.count() == initial_role_count
                assert Park.query.count() == initial_park_count
                assert User.query.count() == initial_user_count
    
    def test_seed_dev_data_requires_password_env_var(self, app):
        """Test that seed_dev_data raises error if SEED_ADMIN_PASSWORD not set"""
        with app.app_context():
            from app import db
            
            # Clear existing data
            User.query.delete()
            Park.query.delete()
            Role.query.delete()
            db.session.commit()
            
            # Remove env var completely
            env_copy = os.environ.copy()
            if 'SEED_ADMIN_PASSWORD' in env_copy:
                del env_copy['SEED_ADMIN_PASSWORD']
            
            with patch.dict(os.environ, env_copy, clear=True):
                # Should raise ValueError
                with pytest.raises(ValueError) as exc_info:
                    seed_dev_data()
                
                assert 'SEED_ADMIN_PASSWORD' in str(exc_info.value)
    
    def test_seed_dev_data_admin_users_have_correct_role(self, app):
        """Test that admin users are assigned to admin role"""
        with app.app_context():
            from app import db
            
            # Clear existing data
            User.query.delete()
            Park.query.delete()
            Role.query.delete()
            db.session.commit()
            
            with patch.dict(os.environ, {'SEED_ADMIN_PASSWORD': 'test_pass'}):
                seed_dev_data()
            
            # Get admin users
            admin1 = User.query.filter_by(email='admin1@example.com').first()
            admin2 = User.query.filter_by(email='admin2@example.com').first()
            
            # Verify they have admin role
            assert admin1.role.name == 'admin'
            assert admin2.role.name == 'admin'
            
            # Verify has_role method works
            assert admin1.has_role('admin') == True
            assert admin2.has_role('admin') == True
    
    def test_seed_dev_data_parks_have_unique_slugs(self, app):
        """Test that all parks have unique slugs"""
        with app.app_context():
            from app import db
            
            # Clear existing data
            User.query.delete()
            Park.query.delete()
            Role.query.delete()
            db.session.commit()
            
            with patch.dict(os.environ, {'SEED_ADMIN_PASSWORD': 'test_pass'}):
                seed_dev_data()
            
            parks = Park.query.all()
            slugs = [park.slug for park in parks]
            
            # All slugs should be unique
            assert len(slugs) == len(set(slugs))
            
            # Verify expected slugs
            assert 'park-1-dublin' in slugs
            assert 'park-2-london' in slugs
            assert 'park-3-berlin' in slugs
    
    def test_seed_dev_data_parks_have_descriptions(self, app):
        """Test that all parks have both short and long descriptions"""
        with app.app_context():
            from app import db
            
            # Clear existing data
            User.query.delete()
            Park.query.delete()
            Role.query.delete()
            db.session.commit()
            
            with patch.dict(os.environ, {'SEED_ADMIN_PASSWORD': 'test_pass'}):
                seed_dev_data()
            
            parks = Park.query.all()
            
            for park in parks:
                # Check description exists and has content
                assert park.description is not None
                assert len(park.description) > 50
                
                # Check short description exists
                assert park.short_description is not None
                assert len(park.short_description) > 10
                
                # Short description should be shorter than full description
                assert len(park.short_description) < len(park.description)
    
    def test_seed_dev_data_parks_have_valid_data_types(self, app):
        """Test that park fields have correct data types"""
        with app.app_context():
            from app import db
            
            # Clear existing data
            User.query.delete()
            Park.query.delete()
            Role.query.delete()
            db.session.commit()
            
            with patch.dict(os.environ, {'SEED_ADMIN_PASSWORD': 'test_pass'}):
                seed_dev_data()
            
            parks = Park.query.all()
            
            for park in parks:
                # String fields
                assert isinstance(park.name, str)
                assert isinstance(park.location, str)
                assert isinstance(park.slug, str)
                assert isinstance(park.difficulty, str)
                
                # Integer field
                assert isinstance(park.min_age, int)
                assert park.min_age > 0
                
                # Check difficulty values are valid
                assert park.difficulty in ['Easy', 'Moderate', 'Hard']
    
    def test_seed_dev_data_with_custom_password(self, app):
        """Test seeding with a custom admin password"""
        with app.app_context():
            from app import db
            
            # Clear existing data
            User.query.delete()
            Park.query.delete()
            Role.query.delete()
            db.session.commit()
            
            custom_password = 'MyCustomAdminPass123!@#'
            
            with patch.dict(os.environ, {'SEED_ADMIN_PASSWORD': custom_password}):
                seed_dev_data()
            
            # Verify both admins can authenticate with custom password
            admin1 = User.query.filter_by(email='admin1@example.com').first()
            admin2 = User.query.filter_by(email='admin2@example.com').first()
            
            assert check_password_hash(admin1.password, custom_password)
            assert check_password_hash(admin2.password, custom_password)
            
            # Verify wrong password doesn't work
            assert not check_password_hash(admin1.password, 'wrong_password')
    
    def test_seed_dev_data_customer_role_exists(self, app):
        """Test that customer role is created but has no users"""
        with app.app_context():
            from app import db
            
            # Clear existing data
            User.query.delete()
            Park.query.delete()
            Role.query.delete()
            db.session.commit()
            
            with patch.dict(os.environ, {'SEED_ADMIN_PASSWORD': 'test_pass'}):
                seed_dev_data()
            
            # Verify customer role exists
            customer_role = Role.query.filter_by(name='customer').first()
            assert customer_role is not None
            
            # Verify no users assigned to customer role yet
            customer_users = User.query.filter_by(role_id=customer_role.role_id).all()
            assert len(customer_users) == 0


class TestSeedDataIntegration:
    """Integration tests for seed data with application startup"""
    
    def test_seed_data_idempotency(self, app):
        """Test that calling seed_dev_data multiple times is safe"""
        with app.app_context():
            from app import db
            
            # Clear existing data
            User.query.delete()
            Park.query.delete()
            Role.query.delete()
            db.session.commit()
            
            with patch.dict(os.environ, {'SEED_ADMIN_PASSWORD': 'test_pass'}):
                # Call multiple times
                seed_dev_data()
                seed_dev_data()
                seed_dev_data()
                
                # Should still only have expected counts
                assert Role.query.count() == 2
                assert User.query.count() == 2
                assert Park.query.count() == 3
    
    def test_seed_data_relationships(self, app):
        """Test that relationships between models work correctly"""
        with app.app_context():
            from app import db
            
            # Clear existing data
            User.query.delete()
            Park.query.delete()
            Role.query.delete()
            db.session.commit()
            
            with patch.dict(os.environ, {'SEED_ADMIN_PASSWORD': 'test_pass'}):
                seed_dev_data()
            
            # Test role-user relationship
            admin_role = Role.query.filter_by(name='admin').first()
            assert len(admin_role.users) == 2
            
            # Test user-role relationship
            admin1 = User.query.filter_by(email='admin1@example.com').first()
            assert admin1.role.name == 'admin'
    
    def test_seed_data_with_subsequent_user_registration(self, app):
        """Test that seeded data doesn't interfere with new user registration"""
        with app.app_context():
            from app import db
            
            # Clear existing data
            User.query.delete()
            Park.query.delete()
            Role.query.delete()
            db.session.commit()
            
            with patch.dict(os.environ, {'SEED_ADMIN_PASSWORD': 'test_pass'}):
                seed_dev_data()
            
            # Now register a new customer user
            customer_role = Role.query.filter_by(name='customer').first()
            new_user = User(
                name='New',
                last_name='Customer',
                email='customer@example.com',
                password=generate_password_hash('customer_pass', method='pbkdf2:sha256'),
                role_id=customer_role.role_id
            )
            db.session.add(new_user)
            db.session.commit()
            
            # Verify counts
            assert User.query.count() == 3  # 2 admins + 1 customer
            assert User.query.filter_by(role_id=customer_role.role_id).count() == 1