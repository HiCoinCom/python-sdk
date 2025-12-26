"""
ChainUp Custody SDK Exceptions

Defines a hierarchy of custom exceptions for better error handling.
"""
from typing import Optional, Dict, Any


class ChainUpError(Exception):
    """
    Base exception for all ChainUp Custody SDK errors.
    
    Attributes:
        message: Human-readable error message
        code: Error code (optional)
        details: Additional error details (optional)
    """
    
    def __init__(
        self,
        message: str,
        code: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self) -> str:
        if self.code is not None:
            return f"[{self.code}] {self.message}"
        return self.message
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message={self.message!r}, code={self.code!r})"


class ConfigError(ChainUpError):
    """
    Raised when there's a configuration error.
    
    Examples:
        - Missing required configuration
        - Invalid configuration values
        - Malformed keys
    """
    pass


class CryptoError(ChainUpError):
    """
    Raised when encryption/decryption operations fail.
    
    Examples:
        - Invalid RSA key format
        - Encryption failure
        - Decryption failure
        - Signature verification failure
    """
    pass


class ApiError(ChainUpError):
    """
    Raised when API requests fail.
    
    Attributes:
        message: Error message from API
        code: API error code
        http_status: HTTP status code (optional)
        request_id: Request ID for tracking (optional)
    """
    
    def __init__(
        self,
        message: str,
        code: Optional[int] = None,
        http_status: Optional[int] = None,
        request_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, details)
        self.http_status = http_status
        self.request_id = request_id
    
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"message={self.message!r}, "
            f"code={self.code!r}, "
            f"http_status={self.http_status!r})"
        )


class NetworkError(ChainUpError):
    """
    Raised when network communication fails.
    
    Examples:
        - Connection timeout
        - DNS resolution failure
        - SSL/TLS errors
    """
    pass


class ValidationError(ChainUpError):
    """
    Raised when request/response validation fails.
    
    Examples:
        - Missing required parameters
        - Invalid parameter types
        - Response parsing errors
    """
    
    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, details=details)
        self.field = field


class SignatureError(CryptoError):
    """
    Raised when transaction signing fails.
    
    Examples:
        - Missing signing key
        - Invalid transaction data
        - Signing operation failure
    """
    pass


class AuthenticationError(ApiError):
    """
    Raised when authentication fails.
    
    Examples:
        - Invalid app_id
        - Invalid signature
        - Expired credentials
    """
    pass


class RateLimitError(ApiError):
    """
    Raised when API rate limit is exceeded.
    
    Attributes:
        retry_after: Seconds to wait before retrying (optional)
    """
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after
