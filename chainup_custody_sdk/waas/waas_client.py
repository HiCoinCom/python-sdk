"""
WaaS Client - Main entry point for WaaS API operations
Provides factory methods for creating API instances
Uses Builder pattern for flexible configuration
"""
from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from chainup_custody_sdk.waas.waas_config import WaasConfig
from chainup_custody_sdk.logger import get_logger, LoggerMixin

if TYPE_CHECKING:
    from chainup_custody_sdk.utils.crypto_provider import ICryptoProvider
    from chainup_custody_sdk.waas.api.user_api import UserApi
    from chainup_custody_sdk.waas.api.account_api import AccountApi
    from chainup_custody_sdk.waas.api.billing_api import BillingApi
    from chainup_custody_sdk.waas.api.coin_api import CoinApi
    from chainup_custody_sdk.waas.api.transfer_api import TransferApi
    from chainup_custody_sdk.waas.api.async_notify_api import AsyncNotifyApi


class WaasClient(LoggerMixin):
    """
    WaaS Client - Main entry point for WaaS API operations.
    
    Provides factory methods for creating API instances.
    Supports context manager protocol for resource management.
    
    Example:
        # Using builder pattern
        client = (
            WaasClient.builder()
            .set_app_id("your-app-id")
            .set_private_key("your-private-key")
            .set_public_key("chainup-public-key")
            .build()
        )
        
        # Using context manager
        with WaasClient.builder().set_app_id("...").build() as client:
            user_api = client.get_user_api()
            # ... use API
    """
    
    __slots__ = ("config", "_closed")

    def __init__(self, config: WaasConfig) -> None:
        """
        Creates a new WaasClient instance.
        
        Args:
            config: WaaS configuration object
        
        Note:
            Prefer using WaasClient.builder() for construction.
        """
        self.config = config
        self._closed = False
        self.config.validate()
        self._logger.debug(f"WaasClient initialized with app_id={config.app_id}")

    def __enter__(self) -> "WaasClient":
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager."""
        self.close()

    def close(self) -> None:
        """
        Close the client and release resources.
        
        This method is called automatically when using context manager.
        """
        if not self._closed:
            self._closed = True
            self._logger.debug("WaasClient closed")

    def get_user_api(self) -> "UserApi":
        """
        Gets UserApi instance for user-related operations.

        Returns:
            UserApi instance
        """
        from chainup_custody_sdk.waas.api.user_api import UserApi
        return UserApi(self.config)

    def get_account_api(self) -> "AccountApi":
        """
        Gets AccountApi instance for account-related operations.

        Returns:
            AccountApi instance
        """
        from chainup_custody_sdk.waas.api.account_api import AccountApi
        return AccountApi(self.config)

    def get_billing_api(self) -> "BillingApi":
        """
        Gets BillingApi instance for billing and transaction operations.

        Returns:
            BillingApi instance
        """
        from chainup_custody_sdk.waas.api.billing_api import BillingApi
        return BillingApi(self.config)

    def get_coin_api(self) -> "CoinApi":
        """
        Gets CoinApi instance for coin and blockchain operations.

        Returns:
            CoinApi instance
        """
        from chainup_custody_sdk.waas.api.coin_api import CoinApi
        return CoinApi(self.config)

    def get_transfer_api(self) -> "TransferApi":
        """
        Gets TransferApi instance for transfer operations.

        Returns:
            TransferApi instance
        """
        from chainup_custody_sdk.waas.api.transfer_api import TransferApi
        return TransferApi(self.config)

    def get_async_notify_api(self) -> "AsyncNotifyApi":
        """
        Gets AsyncNotifyApi instance for async notification operations.

        Returns:
            AsyncNotifyApi instance
        """
        from chainup_custody_sdk.waas.api.async_notify_api import AsyncNotifyApi
        return AsyncNotifyApi(self.config)

    @staticmethod
    def builder() -> "WaasClientBuilder":
        """
        Creates a new Builder instance for configuring WaasClient.

        Returns:
            Builder instance
        
        Example:
            client = WaasClient.builder().set_app_id("...").build()
        """
        return WaasClientBuilder()
    
    @staticmethod
    def new_builder() -> "WaasClientBuilder":
        """
        Creates a new Builder instance (alias for builder()).
        
        Returns:
            Builder instance
        """
        return WaasClientBuilder()


class WaasClientBuilder:
    """
    Builder class for constructing WaasClient instances.
    
    Implements the Builder pattern for flexible configuration.
    All setter methods return self for method chaining.
    
    Example:
        client = (
            WaasClientBuilder()
            .set_app_id("your-app-id")
            .set_private_key("your-private-key")
            .set_public_key("chainup-public-key")
            .set_debug(True)
            .build()
        )
    """
    
    __slots__ = ("_options",)

    def __init__(self) -> None:
        """Creates a new Builder instance."""
        self._options: dict = {}

    def set_host(self, host: str) -> "WaasClientBuilder":
        """
        Sets the API host URL.

        Args:
            host: API host URL

        Returns:
            This builder instance for chaining
        """
        self._options["host"] = host
        return self

    def set_app_id(self, app_id: str) -> "WaasClientBuilder":
        """
        Sets the application ID.

        Args:
            app_id: Application ID

        Returns:
            This builder instance for chaining
        """
        self._options["app_id"] = app_id
        return self

    def set_private_key(self, private_key: str) -> "WaasClientBuilder":
        """
        Sets the RSA private key.

        Args:
            private_key: RSA private key

        Returns:
            This builder instance for chaining
        """
        self._options["private_key"] = private_key
        return self

    def set_public_key(self, public_key: str) -> "WaasClientBuilder":
        """
        Sets the ChainUp public key.

        Args:
            public_key: ChainUp public key

        Returns:
            This builder instance for chaining
        """
        self._options["public_key"] = public_key
        return self

    def set_crypto_provider(self, crypto_provider: "ICryptoProvider") -> "WaasClientBuilder":
        """
        Sets a custom crypto provider for encryption/decryption.

        Args:
            crypto_provider: Custom crypto provider implementation

        Returns:
            This builder instance for chaining
        """
        self._options["crypto_provider"] = crypto_provider
        return self

    def set_version(self, version: str) -> "WaasClientBuilder":
        """
        Sets the API version.

        Args:
            version: API version (default: 'v2')

        Returns:
            This builder instance for chaining
        """
        self._options["version"] = version
        return self

    def set_charset(self, charset: str) -> "WaasClientBuilder":
        """
        Sets the charset encoding.

        Args:
            charset: Charset encoding (default: 'UTF-8')

        Returns:
            This builder instance for chaining
        """
        self._options["charset"] = charset
        return self

    def set_debug(self, debug: bool) -> "WaasClientBuilder":
        """
        Enables or disables debug mode.

        Args:
            debug: Debug flag

        Returns:
            This builder instance for chaining
        """
        self._options["debug"] = debug
        return self

    def build(self) -> WaasClient:
        """
        Builds and returns a configured WaasClient instance.

        Returns:
            Configured WaasClient instance

        Raises:
            ConfigError: If required configuration is missing
        """
        config = WaasConfig(**self._options)
        return WaasClient(config)
