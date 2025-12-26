"""
WaaS Configuration Class
Stores configuration parameters for WaaS (Wallet-as-a-Service) API client
"""
from typing import Optional
from chainup_custody_sdk.utils.crypto_provider import ICryptoProvider


class WaasConfig:
    """
    WaaS Configuration Class.
    Stores configuration parameters for WaaS API client.
    """

    def __init__(
        self,
        host: Optional[str] = None,
        app_id: Optional[str] = None,
        private_key: Optional[str] = None,
        public_key: Optional[str] = None,
        crypto_provider: Optional[ICryptoProvider] = None,
        version: str = "v2",
        charset: str = "UTF-8",
        debug: bool = False,
    ):
        """
        Creates a new WaaS configuration.

        Args:
            host: API host URL
            app_id: Application ID
            private_key: RSA private key for signing requests (required if no crypto_provider)
            public_key: ChainUp public key for verifying responses (required if no crypto_provider)
            crypto_provider: Custom crypto provider implementation
            version: API version (default: 'v2')
            charset: Request charset encoding (default: 'UTF-8')
            debug: Enable debug mode (default: False)
        """
        self.host = host or "https://openapi.chainup.com/"
        self.app_id = app_id or ""
        self.private_key = private_key or ""
        self.public_key = public_key or ""
        self.crypto_provider = crypto_provider
        self.version = version
        self.charset = charset
        self.debug = debug

    def validate(self) -> bool:
        """
        Validates the configuration.

        Returns:
            True if configuration is valid

        Raises:
            ValueError: If required fields are missing
        """
        if not self.host:
            raise ValueError("WaasConfig: host is required")
        if not self.app_id:
            raise ValueError("WaasConfig: app_id is required")

        # Either crypto_provider or private_key/public_key must be provided
        if not self.crypto_provider:
            if not self.private_key:
                raise ValueError(
                    "WaasConfig: private_key is required (or provide crypto_provider)"
                )
            if not self.public_key:
                raise ValueError(
                    "WaasConfig: public_key is required (or provide crypto_provider)"
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
        return f"{self.host}{self.version}{path}"
