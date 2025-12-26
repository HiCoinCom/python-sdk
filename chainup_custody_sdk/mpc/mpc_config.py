"""
MPC Configuration Class
Stores configuration parameters for MPC (Multi-Party Computation) API client
"""
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

from chainup_custody_sdk.exceptions import ConfigError

if TYPE_CHECKING:
    from chainup_custody_sdk.utils.crypto_provider import ICryptoProvider


@dataclass
class MpcConfig:
    """
    MPC Configuration Class.
    
    Stores configuration parameters for MPC API client.
    Uses dataclass for clean, immutable configuration.
    
    Attributes:
        app_id: Application ID
        rsa_private_key: RSA private key for encrypting requests
        waas_public_key: WaaS server public key for decrypting responses
        sign_private_key: RSA private key for transaction signing
        domain: API domain URL
        api_key: API key for authentication
        crypto_provider: Custom crypto provider implementation
        debug: Enable debug mode
    
    Example:
        config = MpcConfig(
            app_id="your-app-id",
            rsa_private_key="your-private-key",
            waas_public_key="waas-public-key",
            sign_private_key="your-sign-key"
        )
    """
    
    app_id: str
    rsa_private_key: str = ""
    waas_public_key: str = ""
    sign_private_key: str = ""
    domain: str = "https://openapi.chainup.com/"
    api_key: str = ""
    crypto_provider: Optional["ICryptoProvider"] = None
    debug: bool = False
    
    def __post_init__(self) -> None:
        """Post-initialization processing."""
        # Normalize domain URL
        if self.domain and not self.domain.endswith("/"):
            object.__setattr__(self, "domain", self.domain + "/")
    
    def validate(self) -> bool:
        """
        Validates the configuration.
        
        Returns:
            True if configuration is valid
        
        Raises:
            ConfigError: If required fields are missing or invalid
        """
        if not self.domain:
            raise ConfigError("MpcConfig: domain is required")
        if not self.app_id:
            raise ConfigError("MpcConfig: app_id is required")
        
        # Either crypto_provider or rsa_private_key must be provided
        if not self.crypto_provider and not self.rsa_private_key:
            raise ConfigError(
                "MpcConfig: rsa_private_key is required (or provide crypto_provider)"
            )
        
        return True
    
    def get_url(self, path: str) -> str:
        """
        Gets the full API URL.
        
        Args:
            path: API path
        
        Returns:
            Full API URL
        """
        # Remove leading slash if present
        path = path.lstrip("/")
        return f"{self.domain}{path}"
    
    @classmethod
    def from_dict(cls, data: dict) -> "MpcConfig":
        """
        Create MpcConfig from dictionary.
        
        Args:
            data: Configuration dictionary
        
        Returns:
            MpcConfig instance
        """
        return cls(
            app_id=data.get("app_id", ""),
            rsa_private_key=data.get("rsa_private_key", ""),
            waas_public_key=data.get("waas_public_key", ""),
            sign_private_key=data.get("sign_private_key", ""),
            domain=data.get("domain", "https://openapi.chainup.com/"),
            api_key=data.get("api_key", ""),
            debug=data.get("debug", False)
        )
