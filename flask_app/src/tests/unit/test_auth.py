"""
Unit tests for authentication
"""
import pytest
from werkzeug.security import generate_password_hash, check_password_hash

class TestAuthentication:
    """Test authentication functions"""
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        password = 'testpassword123'
        hashed = generate_password_hash(password, method='pbkdf2:sha256')
        
        assert hashed != password
        assert check_password_hash(hashed, password)
        assert not check_password_hash(hashed, 'wrongpassword')
    
    def test_password_hash_uniqueness(self):
        """Test that same password generates different hashes"""
        password = 'samepassword'
        hash1 = generate_password_hash(password, method='pbkdf2:sha256')
        hash2 = generate_password_hash(password, method='pbkdf2:sha256')
        
        # Hashes should be different
        assert hash1 != hash2
        # But both should verify correctly
        assert check_password_hash(hash1, password)
        assert check_password_hash(hash2, password)
    
    def test_empty_password(self):
        """Test handling of empty password"""
        password = ''
        hashed = generate_password_hash(password, method='pbkdf2:sha256')
        assert check_password_hash(hashed, password)