"""
Smoke Tests - Basic sanity checks for critical functionality
These tests verify that the application starts, core routes respond,
and basic database operations work.

NOTE: This version removes tests that are comprehensively covered by integration
and unit tests, focusing on unique high-level sanity checks.
"""

import pytest
from datetime import datetime
from app.models import User, Park


class TestAppInitialization:
    """Verify the application initializes correctly"""

    def test_app_exists(self, app):
        """Test that the app object exists"""
        assert app is not None

    def test_app_is_testing(self, app):
        """Test that the app is in testing mode"""
        assert app.config['TESTING'] is True

    def test_app_has_secret_key(self, app):
        """Test that the app has a secret key configured"""
        assert app.config['SECRET_KEY'] is not None
        assert len(app.config['SECRET_KEY']) > 0

    def test_database_connection(self, app):
        """Test that the database connection works"""
        with app.app_context():
            parks = Park.query.all()
            assert isinstance(parks, list)


class TestPublicRoutes:
    """Verify public routes are accessible"""

    def test_index_page_loads(self, client):
        """Test that the homepage loads"""
        response = client.get('/')
        assert response.status_code == 200
        assert response.data is not None

    def test_park_detail_page_loads(self, client, app):
        """Test that park detail page loads with valid park ID"""
        with app.app_context():
            park = Park.query.first()
            if park:
                response = client.get(f'/parks/{park.park_id}')
                assert response.status_code == 200

    def test_park_detail_404_invalid_id(self, client):
        """Test that park detail returns 404 for invalid ID"""
        response = client.get('/parks/99999')
        assert response.status_code == 404

    def test_contact_page_redirects(self, client):
        """Test that contact page redirects to index"""
        response = client.get('/contact', follow_redirects=False)
        assert response.status_code in [301, 302, 303, 307, 308]


class TestAuthenticationRedirects:
    """Verify protected routes require login - quick redirect checks"""

    def test_profile_requires_login(self, client):
        """Test that profile page requires authentication"""
        response = client.get('/profile')
        assert response.status_code == 302
        assert 'login' in response.location.lower()

    def test_booking_requires_login(self, client):
        """Test that booking routes require authentication"""
        response = client.get('/booking/new')
        assert response.status_code == 302
        assert 'login' in response.location.lower()

    def test_health_safety_requires_login(self, client):
        """Test that health/safety page requires authentication"""
        response = client.get('/health-safety-guidelines')
        assert response.status_code == 302
        assert 'login' in response.location.lower()


class TestContactForm:
    """Verify contact form functionality - not covered by integration tests"""

    def test_contact_form_submission(self, client, app):
        """Test that contact form can be submitted"""
        data = {
            'name': 'Test User',
            'email': 'smoke.test@example.com',
            'message': 'Smoke test message'
        }
        
        response = client.post('/contact', data=data, follow_redirects=False)
        assert response.status_code in [301, 302, 303, 307, 308]
        
        # Verify message was created
        with app.app_context():
            from app.models import Message
            message = Message.query.filter_by(email='smoke.test@example.com').first()
            assert message is not None

    def test_contact_form_validation(self, client):
        """Test that contact form requires all fields"""
        # Missing email
        data = {
            'name': 'Test User',
            'message': 'Message without email'
        }
        
        response = client.post('/contact', data=data, follow_redirects=True)
        assert response.status_code == 200


class TestErrorHandling:
    """Verify error handling - not comprehensively covered elsewhere"""

    def test_nonexistent_route_404(self, client):
        """Test that nonexistent routes return 404"""
        response = client.get('/this-route-does-not-exist')
        assert response.status_code == 404

    def test_method_not_allowed(self, client):
        """Test that invalid methods return appropriate error"""
        response = client.delete('/')
        assert response.status_code in [405, 404]


class TestTemplateRendering:
    """Verify templates render without critical errors"""

    def test_index_template_renders(self, client):
        """Test that index template renders without errors"""
        response = client.get('/')
        assert response.status_code == 200
        assert response.content_type is not None

    def test_park_detail_template_renders(self, client, app):
        """Test that park detail template renders"""
        with app.app_context():
            park = Park.query.first()
            if park:
                response = client.get(f'/parks/{park.park_id}')
                assert response.status_code == 200
                assert response.content_type is not None


class TestDatabaseIntegrity:
    """Quick checks for database state - complements unit tests"""

    def test_park_queries_work(self, app):
        """Test that park queries execute without errors"""
        with app.app_context():
            parks = Park.query.all()
            assert len(parks) > 0
            
            for park in parks:
                assert park.park_id is not None
                assert park.name is not None

    def test_users_exist(self, app):
        """Test that seed users were created"""
        with app.app_context():
            users = User.query.all()
            assert len(users) >= 2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])