"""
Integration tests for main routes
"""
import pytest
import sys
import os
from datetime import datetime

# Add the main directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'main'))

class TestMainRoutes:
    """Test main blueprint routes"""
    
    def test_index_page(self, client):
        """Test GET /"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_profile_requires_login(self, client):
        """
        Test that /profile requires authentication
        
         - unauthenticated users cannot access /profile and are redirected to login.
        """
        response = client.get('/profile')
        assert response.status_code == 302  # Redirect to login
        assert '/login' in response.location
    
    def test_profile_authenticated(self, authenticated_client):
        """
        Test /profile when authenticated
        
        - authenticated users return successful operation (code 200)
        - check correct data returned
        """
        response = authenticated_client.get('/profile')
        assert response.status_code == 200
        assert b'Test' in response.data  # User's name
    
    def test_view_bookings_requires_login(self, client):
        """
        Test that /bookings requires authentication

         - unauthenticated users cannot access /profile and are redirected to login.
        """
        response = client.get('/bookings')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_view_bookings_authenticated_empty(self, authenticated_client):
        """
        Test viewing bookings when no bookings exist
        
        - good response if authenticated user (code 200)
        """
        response = authenticated_client.get('/bookings')
        assert response.status_code == 200
    
    def test_view_bookings_with_data(self, authenticated_client, app):
        """
        Test viewing bookings when bookings exist

        - creates a test booking in the database
        - checks if the bookings page returns a successful response (code 200) for authenticated users.
        """
        # Create a test booking first
        with app.app_context():
            from app import db
            from app.models import User, Park, Booking

            user = User.query.filter_by(email='test@example.com').first()
            park = Park.query.first()

            booking = Booking(
                user_id=user.user_id,
                park_id=park.park_id,
                date=datetime(2026, 8, 1),
                num_tickets=2,
                health_safety=True
            )
            db.session.add(booking)
            db.session.commit()

        response = authenticated_client.get('/bookings')
        assert response.status_code == 200

    def test_new_booking_page_requires_login(self, client):
        """
        Test that /booking/new requires authentication

        - unauthenticated users cannot access /booking/new and are redirected to login.
        """
        response = client.get('/booking/new')
        assert response.status_code == 302
        assert '/login' in response.location

    def test_new_booking_page_authenticated(self, authenticated_client):
        """
        Test GET /booking/new when authenticated

        - authenticated users can access the new booking page (code 200).
        """
        response = authenticated_client.get('/booking/new')
        assert response.status_code == 200

    def test_create_booking_requires_login(self, client, app):
        """
        Test that POST /booking requires authentication

        - unauthenticated users cannot submit a booking and are redirected to login.
        """
        with app.app_context():
            from app.models import Park
            park = Park.query.first()

            response = client.post('/booking', data={
                'park_id': park.park_id,
                'date': '2026-09-15T10:00',
                'num_tickets': '3',
                'health_safety': 'on'
            })

            assert response.status_code == 302
            assert '/login' in response.location

    def test_create_booking_success(self, authenticated_client, app):
        """
        Test POST /booking with valid data

        - authenticated users can successfully create a booking with valid data
        - checks if the booking count increases and details match the submitted data.
        """
        with app.app_context():
            from app.models import Park, User, Booking
            park = Park.query.first()
            user = User.query.filter_by(email='test@example.com').first()
            initial_count = Booking.query.filter_by(user_id=user.user_id).count()

            response = authenticated_client.post('/booking', data={
                'park_id': park.park_id,
                'date': '2026-09-15T10:00',
                'num_tickets': '3',
                'health_safety': 'on'
            }, follow_redirects=True)

            assert response.status_code == 200

            # Verify booking was created
            final_count = Booking.query.filter_by(user_id=user.user_id).count()
            assert final_count == initial_count + 1

            # Verify booking details
            booking = Booking.query.filter_by(user_id=user.user_id).order_by(Booking.booking_id.desc()).first()
            assert booking.num_tickets == 3
            assert booking.health_safety == True

    def test_create_booking_without_health_safety(self, authenticated_client, app):
        """
        Test creating booking without health_safety checkbox

        - checks if health_safety defaults to False when not provided.
        """
        with app.app_context():
            from app.models import Park, User, Booking
            park = Park.query.first()

            response = authenticated_client.post('/booking', data={
                'park_id': park.park_id,
                'date': '2026-10-01T14:00',
                'num_tickets': '1'
            }, follow_redirects=True)

            assert response.status_code == 200

            # Verify booking was created with health_safety=False
            user = User.query.filter_by(email='test@example.com').first()
            booking = Booking.query.filter_by(user_id=user.user_id).order_by(Booking.booking_id.desc()).first()
            assert booking.health_safety == False

    def test_404_error_handler(self, client):
        """
        Test 404 error handler

        - checks if non-existent routes return a 404 error.
        """
        response = client.get('/nonexistent-page-12345')
        assert response.status_code == 404
