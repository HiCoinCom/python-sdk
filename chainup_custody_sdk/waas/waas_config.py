"""
WaaS Configuration Class
Stores configuration parameters for WaaS (Wallet-as-a-Service) API client
"""
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

from chainup_custody_sdk.exceptions import ConfigError

if TYPE_CHECKING:
    from chainup_custody_sdk.utils.crypto_provider import ICryptoProvider


@dataclass
class WaasConfig:
    """
    WaaS Configuration Class.
    
    Stores configuration parameters for WaaS API client.
    Uses dataclass for clean, immutable configuration.
    
    Attributes:
        host: API host URL
        app_id: Application ID
        private_key: RSA private key for signing requests
        public_key: ChainUp public key for verifying responses
        crypto_provider: Custom crypto provider implementation
        version: API version
        charset: Request charset encoding
        debug: Enable debug mode
    
    Example:
        config = WaasConfig(
            host="https://openapi.chainup.com/",
            app_id="your-app-id",
            private_key="your-private-key",
            public_key="chainup-public-key"
        )
    """
    
    app_id: str
    private_key: str = ""
    public_key: str = ""
    host: str = "https://openapi.chainup.com/"
    crypto_provider: Optional["ICryptoProvider"] = None
    version: str = "v2"
    charset: str = "UTF-8"
    debug: bool = False
    
    def __post_init__(self) -> None:
        """Post-initialization processing."""
        # Normalize host URL
        if self.host and not self.host.endswith("/"):
            object.__setattr__(self, "host", self.host + "/")
    
    def validate(self) -> bool:
        """
        Validates the configuration.
        
        Returns:
            True if configuration is valid
        
        Raises:
            ConfigError: If required fields are missing or invalid
        """
        if not self.host:
            raise ConfigError("WaasConfig: host is required")
        if not self.app_id:
            raise ConfigError("WaasConfig: app_id is required")
        
        # Either crypto_provider or private_key/public_key must be provided
        if not self.crypto_provider:
            if not self.private_key:
                raise ConfigError(
                    "WaasConfig: private_key is required (or provide crypto_provider)"
                )
            if not self.public_key:
                raise ConfigError(
                    "WaasConfig: public_key is required (or provide crypto_provider)"
                )
        
        return True
    
    def get_url(self, path: str) -> str:
        """
        Gets the full API URL.
        
        Args:
            path: API path (without leading slash for v2 prefix)
        
        Returns:
            Full API URL
        """
        # Remove leading slash if present
        path = path.lstrip("/")
        return f"{self.host}{self.version}/{path}"
    
    @classmethod
    def from_dict(cls, data: dict) -> "WaasConfig":
        """
        Create WaasConfig from dictionary.
        
        Args:
            data: Configuration dictionary
        
        Returns:
            WaasConfig instance
        """
        return cls(
            app_id=data.get("app_id", ""),
            private_key=data.get("private_key", ""),
            public_key=data.get("public_key", ""),
            host=data.get("host", "https://openapi.chainup.com/"),
            version=data.get("version", "v2"),
            charset=data.get("charset", "UTF-8"),
            debug=data.get("debug", False)
        )
