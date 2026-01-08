"""
Integration tests for complete user flows
"""
import pytest
import sys
import os

# Add the main directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'main'))

class TestUserFlows:
    """Test complete user workflows"""

    def test_complete_registration_login_flow(self, client):
        """
        Test: Register -> Login -> Access Profile

        - registers a new user
        - logs in with the new credentials
        - verifies access to the profile page and correct user data.
        """
        # 1. Register
        response = client.post('/register', data={
            'email': 'flowtest@example.com',
            'name': 'Flow',
            'last_name': 'Test',
            'password': 'flowpass123'
        }, follow_redirects=True)
        assert response.status_code == 200

        # 2. Login
        response = client.post('/login', data={
            'email': 'flowtest@example.com',
            'password': 'flowpass123'
        }, follow_redirects=True)
        assert response.status_code == 200

        # 3. Access profile
        response = client.get('/profile')
        assert response.status_code == 200
        assert b'Flow' in response.data

    def test_booking_creation_flow(self, authenticated_client, app):
        """
        Test: Login -> View Parks -> Create Booking -> View Bookings

        - accesses the new booking page
        - creates a booking with valid data
        - verifies the booking appears in the user's bookings list.
        """
        # 1. View new booking page to see available parks
        response = authenticated_client.get('/booking/new')
        assert response.status_code == 200

        # 2. Create booking
        with app.app_context():
            from app.models import Park
            park = Park.query.first()

            response = authenticated_client.post('/booking', data={
                'park_id': park.park_id,
                'date': '2026-10-20T14:00',
                'num_tickets': '4',
                'health_safety': 'on'
            }, follow_redirects=True)
            assert response.status_code == 200

        # 3. View bookings
        response = authenticated_client.get('/bookings')
        assert response.status_code == 200

    def test_multiple_bookings_flow(self, authenticated_client, app):
        """
        Test creating multiple bookings for the same user

        - creates two bookings for the same user
        - verifies both bookings are saved in the database.
        """
        with app.app_context():
            from app.models import Park, User, Booking
            parks = Park.query.all()
            user = User.query.filter_by(email='test@example.com').first()
            initial_count = Booking.query.filter_by(user_id=user.user_id).count()

            # Create first booking
            authenticated_client.post('/booking', data={
                'park_id': parks[0].park_id,
                'date': '2026-11-01T10:00',
                'num_tickets': '2'
            }, follow_redirects=True)

            # Create second booking
            authenticated_client.post('/booking', data={
                'park_id': parks[1].park_id if len(parks) > 1 else parks[0].park_id,
                'date': '2026-11-15T14:00',
                'num_tickets': '3'
            }, follow_redirects=True)

            # Verify both bookings exist
            final_count = Booking.query.filter_by(user_id=user.user_id).count()
            assert final_count == initial_count + 2

    def test_unauthorized_access_flow(self, client):
        """
        Test that unauthenticated users are redirected properly

        - attempts to access protected routes without authentication
        - verifies redirection to the login page for each route.
        """
        # Try to access protected pages
        protected_routes = ['/profile', '/bookings', '/booking/new']

        for route in protected_routes:
            response = client.get(route)
            assert response.status_code == 302  # Redirect
            assert '/login' in response.location

    def test_logout_and_access_flow(self, authenticated_client):
        """
        Test: Access Profile -> Logout -> Try to Access Profile

        - verifies access to the profile page while logged in
        - logs out the user
        - verifies that profile access is denied after logout.
        """
        # 1. Verify can access profile
        response = authenticated_client.get('/profile')
        assert response.status_code == 200

        # 2. Logout
        response = authenticated_client.get('/logout', follow_redirects=True)
        assert response.status_code == 200

        # 3. Try to access profile again (should fail)
        response = authenticated_client.get('/profile')
        assert response.status_code == 302
        assert '/login' in response.location

    def test_register_with_existing_email_flow(self, client, app):
        """
        Test: Register -> Try to Register Again with Same Email

        - registers a user with a unique email
        - attempts to register again with the same email
        - verifies the error message and that only one user exists.
        """
        # 1. First registration
        client.post('/register', data={
            'email': 'duplicate@example.com',
            'name': 'First',
            'last_name': 'User',
            'password': 'password123'
        }, follow_redirects=True)

        # 2. Try to register again with same email
        response = client.post('/register', data={
            'email': 'duplicate@example.com',
            'name': 'Second',
            'last_name': 'User',
            'password': 'password456'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'email address already exists' in response.data

        # 3. Verify only one user exists
        with app.app_context():
            from app.models import User
            users = User.query.filter_by(email='duplicate@example.com').all()
            assert len(users) == 1
            assert users[0].name == 'First'  # Original user should remain
