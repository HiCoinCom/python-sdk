"""
MPC Configuration Class
Stores configuration parameters for MPC (Multi-Party Computation) API client
"""
from typing import Optional
from chainup_custody_sdk.utils.crypto_provider import ICryptoProvider, RsaCryptoProvider


class MpcConfig:
    """
    MPC Configuration Class.
    Stores configuration parameters for MPC API client.
    """

    def __init__(
        self,
        domain: Optional[str] = None,
        app_id: Optional[str] = None,
        rsa_private_key: Optional[str] = None,
        waas_public_key: Optional[str] = None,
        api_key: Optional[str] = None,
        sign_private_key: Optional[str] = None,
        crypto_provider: Optional[ICryptoProvider] = None,
        debug: bool = False,
    ):
        """
        Creates a new MPC configuration.

        Args:
            domain: API domain URL
            app_id: Application ID
            rsa_private_key: RSA private key (required if no crypto_provider)
            waas_public_key: WaaS server public key for decrypting responses
            api_key: API key for authentication
            sign_private_key: RSA private key for transaction signing (optional)
            crypto_provider: Custom crypto provider implementation
            debug: Enable debug mode (default: False)
        """
        self.domain = domain or "https://openapi.chainup.com/"
        self.app_id = app_id or ""
        self.rsa_private_key = rsa_private_key or ""
        self.waas_public_key = waas_public_key or ""
        self.api_key = api_key or ""
        self.sign_private_key = sign_private_key or ""
        self.crypto_provider = crypto_provider
        self.debug = debug

    def validate(self) -> bool:
        """
        Validates the configuration.

        Returns:
            True if configuration is valid

        Raises:
            ValueError: If required fields are missing
        """
        if not self.domain:
            raise ValueError("MpcConfig: domain is required")
        if not self.app_id:
            raise ValueError("MpcConfig: app_id is required")

        # Either crypto_provider or rsa_private_key must be provided
        if not self.crypto_provider and not self.rsa_private_key:
            raise ValueError(
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
        return f"{self.domain}{path}"
