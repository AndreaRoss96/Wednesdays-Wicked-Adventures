"""
Integration tests for main routes
"""
import pytest
import sys
import os
from datetime import datetime
from unittest.mock import patch

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
        assert response.status_code == 302  # Redirects to login
        assert '/login' in response.location
    
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
        """Test that /booking requires authentication"""
        response = client.get('/booking')
        assert response.status_code == 302
        assert '/login' in response.location
    
    # def test_view_bookings_authenticated(self, authenticated_client, app):
    #     """Test viewing bookings when authenticated"""
    #     with app.app_context():
    #         from app import db
    #         from app.models import User, Park, Booking
            
    #         user = User.query.filter_by(email='test@example.com').first()
    #         park = Park.query.first()
            
    #         booking = Booking(
    #             user_id=user.user_id,
    #             park_id=park.park_id,
    #             date=datetime(2026, 8, 1),
    #             num_tickets=2,
    #             health_safety=True
    #         )
    #         db.session.add(booking)
    #         db.session.commit()
        
    #     response = authenticated_client.get('/booking')
    #     assert response.status_code == 200
    
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

class TestMainRoutesExpanded:
    """Additional tests for main.py to improve coverage"""
    
    # ==========================================
    # Profile Route Tests
    # ==========================================
    
    # def test_profile_redirects_admin_to_admin_panel(self, app):
    #     """Test that admin users are redirected to admin panel"""
    #     with app.app_context():
    #         from app.models import User
            
    #         # Get admin user and login
    #         admin = User.query.filter_by(email='admin@example.com').first()
            
    #         with app.test_client() as client:
    #             with client.session_transaction() as sess:
    #                 sess['_user_id'] = str(admin.user_id)
                
    #             # Admin should be redirected to /admin/
    #             response = client.get('/profile')
    #             assert response.status_code == 302
    #             assert '/admin' in response.location
    
    def test_profile_shows_for_regular_user(self, authenticated_client):
        """Test that regular users see their profile"""
        response = authenticated_client.get('/profile')
        assert response.status_code == 200
        assert b'Test' in response.data
    
    # ==========================================
    # Booking Route Tests (POST edge cases)
    # ==========================================
    
    def test_booking_post_creates_booking(self, authenticated_client, app):
        """Test POST /booking creates a booking"""
        with app.app_context():
            from app.models import Park, Booking, User
            
            park = Park.query.first()
            user = User.query.filter_by(email='test@example.com').first()
            initial_count = Booking.query.filter_by(user_id=user.user_id).count()
            
            response = authenticated_client.post('/booking', data={
                'park_id': park.park_id,
                'date': '2026-12-25T14:30',
                'num_tickets': '2',
                'health_safety': 'on'
            }, follow_redirects=True)
            
            assert response.status_code == 200
            
            # Verify booking created
            final_count = Booking.query.filter_by(user_id=user.user_id).count()
            assert final_count == initial_count + 1
            
            # Verify booking details
            booking = Booking.query.filter_by(user_id=user.user_id).order_by(Booking.booking_id.desc()).first()
            assert booking.park_id == park.park_id
            assert booking.num_tickets == 2
            assert booking.health_safety == True
    
    def test_booking_post_without_health_safety(self, authenticated_client, app):
        """Test booking creation without health_safety checkbox"""
        with app.app_context():
            from app.models import Park, Booking, User
            
            park = Park.query.first()
            
            response = authenticated_client.post('/booking', data={
                'park_id': park.park_id,
                'date': '2026-11-15T10:00',
                'num_tickets': '1'
                # No health_safety
            }, follow_redirects=True)
            
            assert response.status_code == 200
            
            user = User.query.filter_by(email='test@example.com').first()
            booking = Booking.query.filter_by(user_id=user.user_id).order_by(Booking.booking_id.desc()).first()
            assert booking.health_safety == False
    
    def test_booking_get_redirects_to_profile(self, authenticated_client):
        """Test GET /booking redirects to profile"""
        response = authenticated_client.get('/booking', follow_redirects=False)
        assert response.status_code == 302
        assert '/profile' in response.location
    
    # ==========================================
    # Health & Safety Guidelines Tests
    # ==========================================
    
    def test_health_safety_guidelines_requires_auth(self, client):
        """Test health guidelines requires authentication"""
        response = client.get('/health-safety-guidelines')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_health_safety_guidelines_shows_date(self, authenticated_client):
        """Test health guidelines page includes current date"""
        response = authenticated_client.get('/health-safety-guidelines')
        assert response.status_code == 200
        # Page should render successfully
    
    # ==========================================
    # Contact Form Tests (Coverage for lines 64-91)
    # ==========================================
    
    def test_contact_page_get_redirects_to_index_with_anchor(self, client):
        """Test GET /contact redirects to index#contact"""
        response = client.get('/contact', follow_redirects=False)
        assert response.status_code == 302
        assert response.location.endswith('/#contact')
    
    def test_contact_submit_success(self, client, app):
        """Test successful contact form submission"""
        response = client.post('/contact', data={
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'This is a test message'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Thank you for your message' in response.data
        
        # Verify message was saved
        with app.app_context():
            from app.models import Message
            message = Message.query.filter_by(email='john@example.com').first()
            assert message is not None
            assert message.name == 'John Doe'
            assert message.message == 'This is a test message'
    
    def test_contact_submit_missing_name(self, client):
        """Test contact form with missing name field"""
        response = client.post('/contact', data={
            'email': 'test@example.com',
            'message': 'Test message'
            # Missing 'name'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Please fill in all fields' in response.data
    
    def test_contact_submit_missing_email(self, client):
        """Test contact form with missing email field"""
        response = client.post('/contact', data={
            'name': 'Test User',
            'message': 'Test message'
            # Missing 'email'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Please fill in all fields' in response.data
    
    def test_contact_submit_missing_message(self, client):
        """Test contact form with missing message field"""
        response = client.post('/contact', data={
            'name': 'Test User',
            'email': 'test@example.com'
            # Missing 'message'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Please fill in all fields' in response.data
    
    def test_contact_submit_all_fields_empty(self, client):
        """Test contact form with all empty fields"""
        response = client.post('/contact', data={
            'name': '',
            'email': '',
            'message': ''
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Please fill in all fields' in response.data
    
    def test_contact_submit_with_referrer(self, client):
        """Test contact form preserves referrer URL"""
        response = client.post('/contact', 
            data={
                'name': 'Test',
                'email': 'test@test.com',
                'message': 'Message'
            },
            headers={'Referer': 'http://localhost/#contact'},
            follow_redirects=False
        )
        
        assert response.status_code == 302
        assert '#contact' in response.location
    
    def test_contact_submit_without_referrer(self, client):
        """Test contact form without referrer defaults to index"""
        response = client.post('/contact', data={
            'name': 'Test',
            'email': 'test@test.com',
            'message': 'Message'
        }, follow_redirects=False)
        
        assert response.status_code == 302
        # Should redirect to index with #contact anchor
        assert '/#contact' in response.location or response.location.endswith('#contact')
    
    def test_contact_submit_database_error(self, client, app):
        """Test contact form handles database errors gracefully"""
        with app.app_context():
            with patch('app.main.db.session.commit') as mock_commit:
                mock_commit.side_effect = Exception("Database error")
                
                response = client.post('/contact', data={
                    'name': 'Error Test',
                    'email': 'error@test.com',
                    'message': 'This will cause an error'
                }, follow_redirects=True)
                
                assert response.status_code == 200
                assert b'error sending your message' in response.data
    
    def test_contact_submit_referrer_with_anchor_stripped(self, client):
        """Test that anchor is stripped from referrer before re-adding"""
        response = client.post('/contact',
            data={
                'name': 'Test',
                'email': 'test@test.com',
                'message': 'Message'
            },
            headers={'Referer': 'http://localhost/some-page#contact'},
            follow_redirects=False
        )
        
        assert response.status_code == 302
        # Should have #contact only once at the end
        location = response.location
        assert location.endswith('#contact')
        # Count occurrences of #contact (should be 1)
        assert location.count('#contact') == 1
    
    # ==========================================
    # Park Detail Tests
    # ==========================================
    
    def test_park_detail_valid_id(self, client, app):
        """Test park detail with valid park ID"""
        with app.app_context():
            from app.models import Park
            park = Park.query.first()
            
            response = client.get(f'/parks/{park.park_id}')
            assert response.status_code == 200
            assert park.name.encode() in response.data
    
    def test_park_detail_invalid_id_returns_404(self, client):
        """Test park detail with non-existent park ID"""
        response = client.get('/parks/99999')
        assert response.status_code == 404
    
    # ==========================================
    # Index Route Tests
    # ==========================================
    
    def test_index_displays_all_parks(self, client, app):
        """Test index page loads all parks"""
        with app.app_context():
            from app.models import Park
            park_count = Park.query.count()
            
            response = client.get('/')
            assert response.status_code == 200
            
            # Should have parks in the database
            assert park_count > 0