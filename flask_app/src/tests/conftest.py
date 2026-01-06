"""
Pytest configuration and definition for fixtures
"""

import pytest
import os
import sys
import tempfile

# Add the main directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'main'))

from app import create_app, db
from app.models import User, Role, Park, Booking
from werkzeug.security import generate_password_hash
from datetime import datetime

@pytest.fixture(scope='session')
def app():
    """
    Simulate application for testing
    """
    # Create a temporary file for the test database
    db_fd, db_path = tempfile.mkstemp()
    
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'test-secret-key',
        'WTF_CSRF_ENABLED': False  # Disable CSRF for testing
    }
    
    app = create_app('testing')
    app.config.update(test_config)
    
    with app.app_context():
        db.create_all()
        _create_test_data()
        
    yield app
    
    # Cleanup
    with app.app_context():
        db.session.remove()
        db.drop_all()
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture(scope='function')
def client(app):
    """
    Create a test client
    """
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app):
    """
    Create a test CLI runner
    """
    return app.test_cli_runner()

@pytest.fixture(scope='function')
def db_session(app):
    """
        Create a new database session for a test
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

        Takes regular user -> add session cookie -> returns logged in client
    """
    with app.app_context():
        user = User.query.filter_by(email='test@example.com').first()
        with client.session_transaction() as sess:
            sess['_user_id'] = str(user.user_id)
    return client

def _create_test_data():
    """
        Create initial test data
    """
    # Create roles
    user_role = Role(role_id=1, name='user')
    admin_role = Role(role_id=2, name='admin')
    db.session.add(user_role)
    db.session.add(admin_role)
    
    # Create test users
    test_user = User(
        name='Test',
        last_name='User',
        email='test@example.com',
        password=generate_password_hash('password123', method='pbkdf2:sha256'),
        role_id=1
    )
    admin_user = User(
        name='Admin',
        last_name='User',
        email='admin@example.com',
        password=generate_password_hash('admin123', method='pbkdf2:sha256'),
        role_id=2
    )
    db.session.add(test_user)
    db.session.add(admin_user)
    
    # Create test parks
    park1 = Park(
        name='Leprechaun Park',
        location='Dublin',
        description='Capital park'
    )
    park2 = Park(
        name='Paddy Park',
        location='Cork',
        description='Real capital park'
    )
    db.session.add(park1)
    db.session.add(park2)
    
    db.session.commit()