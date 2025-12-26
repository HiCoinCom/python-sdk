"""
Unit tests for exceptions module
"""
import pytest
from chainup_custody_sdk.exceptions import (
    ChainUpError,
    ApiError,
    ConfigError,
    CryptoError,
    NetworkError,
    ValidationError,
    SignatureError,
    AuthenticationError,
    RateLimitError,
)


class TestChainUpError:
    """Tests for ChainUpError base exception."""
    
    def test_basic_error(self):
        """Test basic error creation."""
        error = ChainUpError("Test error")
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.code is None
        assert error.details == {}
    
    def test_error_with_code(self):
        """Test error with code."""
        error = ChainUpError("Test error", code=1001)
        assert str(error) == "[1001] Test error"
        assert error.code == 1001
    
    def test_error_with_details(self):
        """Test error with details."""
        details = {"field": "email", "reason": "invalid"}
        error = ChainUpError("Test error", details=details)
        assert error.details == details
    
    def test_repr(self):
        """Test error repr."""
        error = ChainUpError("Test error", code=1001)
        assert "ChainUpError" in repr(error)
        assert "1001" in repr(error)


class TestApiError:
    """Tests for ApiError exception."""
    
    def test_api_error(self):
        """Test API error creation."""
        error = ApiError("Invalid request", code=1001, http_status=400)
        assert error.message == "Invalid request"
        assert error.code == 1001
        assert error.http_status == 400
    
    def test_api_error_with_request_id(self):
        """Test API error with request ID."""
        error = ApiError("Error", request_id="req-123")
        assert error.request_id == "req-123"


class TestConfigError:
    """Tests for ConfigError exception."""
    
    def test_config_error(self):
        """Test config error."""
        error = ConfigError("Missing app_id")
        assert isinstance(error, ChainUpError)
        assert str(error) == "Missing app_id"


class TestCryptoError:
    """Tests for CryptoError exception."""
    
    def test_crypto_error(self):
        """Test crypto error."""
        error = CryptoError("Invalid key format")
        assert isinstance(error, ChainUpError)
        assert str(error) == "Invalid key format"


class TestValidationError:
    """Tests for ValidationError exception."""
    
    def test_validation_error_with_field(self):
        """Test validation error with field."""
        error = ValidationError("Invalid value", field="email")
        assert error.field == "email"
        assert error.message == "Invalid value"


class TestSignatureError:
    """Tests for SignatureError exception."""
    
    def test_signature_error(self):
        """Test signature error inherits from CryptoError."""
        error = SignatureError("Signature verification failed")
        assert isinstance(error, CryptoError)
        assert isinstance(error, ChainUpError)


class TestRateLimitError:
    """Tests for RateLimitError exception."""
    
    def test_rate_limit_error(self):
        """Test rate limit error with retry_after."""
        error = RateLimitError(retry_after=60)
        assert error.retry_after == 60
        assert "Rate limit" in str(error)
