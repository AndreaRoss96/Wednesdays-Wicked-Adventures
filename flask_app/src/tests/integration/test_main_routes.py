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
        """Test GET / loads and shows parks"""
        response = client.get('/')
        assert response.status_code == 200
        # Check for something that IS on the page
        # print(response.data)
        assert b"Wednesday's Wicked Adventures" in response.data
    
    def test_index_displays_all_parks(self, client, app):
        """Test that index shows all parks"""
        response = client.get('/')
        assert response.status_code == 200
        
        with app.app_context():
            from app.models import Park
            parks = Park.query.all()
            assert len(parks) == 3  # Should have 3 parks from seed data
    
    def test_park_detail_page(self, client, app):
        """Test GET /parks/<id> shows park details"""
        with app.app_context():
            from app.models import Park
            park = Park.query.first()
            
            response = client.get(f'/parks/{park.park_id}')
            assert response.status_code == 200
            assert park.name.encode() in response.data
            assert park.location.encode() in response.data
    
    def test_park_detail_not_found(self, client):
        """Test park detail with invalid ID"""
        response = client.get('/parks/99999')
        assert response.status_code == 404
    
    def test_health_safety_guidelines_page(self, client):
        """Test GET /health-safety-guidelines"""
        response = client.get('/health-safety-guidelines')
        assert response.status_code == 200
    
    def test_profile_requires_login(self, client):
        """Test that /profile requires authentication"""
        response = client.get('/profile')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_profile_authenticated(self, authenticated_client):
        """Test /profile when authenticated"""
        response = authenticated_client.get('/profile')
        assert response.status_code == 200
        assert b'Test' in response.data
    
    def test_view_bookings_requires_login(self, client):
        """Test that /bookings requires authentication"""
        response = client.get('/bookings')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_view_bookings_authenticated(self, authenticated_client, app):
        """Test viewing bookings when authenticated"""
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
        """Test that /booking/new requires authentication"""
        response = client.get('/booking/new')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_new_booking_page_authenticated(self, authenticated_client):
        """Test GET /booking/new when authenticated"""
        response = authenticated_client.get('/booking/new')
        assert response.status_code == 200
    
    def test_create_booking_requires_login(self, client, app):
        """Test that POST /booking requires authentication"""
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
        """Test POST /booking with valid data"""
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
        """Test creating booking without health_safety checkbox"""
        with app.app_context():
            from app.models import Park, User, Booking
            park = Park.query.first()
            
            response = authenticated_client.post('/booking', data={
                'park_id': park.park_id,
                'date': '2026-10-01T14:00',
                'num_tickets': '1'
            }, follow_redirects=True)
            
            assert response.status_code == 200
            
            user = User.query.filter_by(email='test@example.com').first()
            booking = Booking.query.filter_by(user_id=user.user_id).order_by(Booking.booking_id.desc()).first()
            assert booking.health_safety == False
    
    def test_404_error_handler(self, client):
        """Test 404 error handler"""
        response = client.get('/nonexistent-page-12345')
        assert response.status_code == 404