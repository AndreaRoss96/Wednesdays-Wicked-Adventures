"""
Pytest configuration and definition for fixtures
"""

import pytest
import os
import sys
import tempfile
import warnings

# Suppress SQLAlchemy deprecation warnings
from sqlalchemy.exc import SADeprecationWarning
warnings.filterwarnings("ignore", category=SADeprecationWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Add the main directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'main'))

from app import create_app, db
from app.models import User, Role, Park, Booking
from werkzeug.security import generate_password_hash
from datetime import datetime

@pytest.fixture(scope='function')
def app():
    """Create application for testing"""
    test_app = create_app('testing')
    
    # Ensure config is applied
    test_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'test-secret-key',
        'WTF_CSRF_ENABLED': False
    })
    
    with test_app.app_context():
        db.create_all()
        # Seed data for each test
        _create_test_data()
        
    yield test_app
    
    # Cleanup
    with test_app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    """
    Create a test client for HTTP requests
    """
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app):
    """
    Create a test CLI runner for command-line testing
    """
    return app.test_cli_runner()

@pytest.fixture(scope='function')
def db_session(app):
    """
    Create a new database session for a test with transaction support
    """
    with app.app_context():
        # Start a transaction
        connection = db.engine.connect()
        transaction = connection.begin()

        # Bind the session to the connection
        options = {"bind": connection}
        session = db.create_scoped_session(options=options)

        # Replace the default session
        db.session = session

        yield session

        # Rollback and cleanup
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture
def authenticated_client(client, app):
    """
    Fixture that provides an authenticated client
    """
    with app.app_context():
        user = User.query.filter_by(email='test@example.com').first()
        if user:  # Only authenticate if test user exists
            with client.session_transaction() as sess:
                sess['_user_id'] = str(user.user_id)
    return client

def _create_test_data():
    """
    Create initial test data: roles, users, and parks
    """
    # Create roles
    user_role = Role(role_id=1, name='user')
    admin_role = Role(role_id=2, name='admin')
    db.session.add(user_role)
    db.session.add(admin_role)
    db.session.commit()

    # Get role IDs after commit
    admin = Role.query.filter_by(name='admin').first()
    user = Role.query.filter_by(name='user').first()

    # Create test users
    test_user = User(
        name='Test',
        last_name='User',
        email='test@example.com',
        password=generate_password_hash('password123', method='pbkdf2:sha256'),
        role_id=user.role_id
    )
    admin_user = User(
        name='Admin',
        last_name='User',
        email='admin@example.com',
        password=generate_password_hash('admin123', method='pbkdf2:sha256'),
        role_id=admin.role_id
    )
    db.session.add(test_user)
    db.session.add(admin_user)

    # Create test parks
    park1 = Park(
        name='Leprechaun Park',
        location='Dublin',
        description='Capital park',
        short_description='Step into a world of spells',
        slug='park-1-dublin',
        image_path='images/parks/witches/hat.png',
        folder='witches',
        hours='10:00 AM - 8:00 PM',
        difficulty='Moderate',
        min_age=10,
        price='Starting at $39.99',
        wait_time='20-40 minutes',
        height_requirement='42" (1.07m)'
    )
    park2 = Park(
        name='Paddy Park',
        location='Cork',
        description='Real capital park',
        short_description='Enter the web of fear',
        slug='park-2-Cork',
        image_path='images/parks/spider/spider.png',
        folder='spider',
        hours='9:00 AM - 10:00 PM',
        difficulty='Hard',
        min_age=14,
        price='Starting at $54.99',
        wait_time='45-75 minutes',
        height_requirement='54" (1.37m)'
    )
    park3 = Park(
        name='Haunted House',
        location='Galway',
        description='Classic haunted manor experience',
        short_description='Walk among the restless dead',
        slug='park-3-Galway',
        image_path='images/parks/haunted/skull.png',
        folder='haunted',
        hours='6:00 PM - 2:00 AM',
        difficulty='Easy',
        min_age=8,
        price='Starting at $29.99',
        wait_time='15-30 minutes',
        height_requirement='None'
    )
    db.session.add_all([park1, park2, park3])
    
    db.session.commit()
