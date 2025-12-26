"""
WaaS Client - Main entry point for WaaS API operations
Provides factory methods for creating API instances
Uses Builder pattern for flexible configuration
"""
from typing import Optional
from chainup_custody_sdk.waas.waas_config import WaasConfig
from chainup_custody_sdk.utils.crypto_provider import ICryptoProvider


class WaasClient:
    """
    WaaS Client - Main entry point for WaaS API operations.
    Provides factory methods for creating API instances.
    """

    def __init__(self, config: WaasConfig):
        """
        Private constructor - use Builder to create instances.

        Args:
            config: WaaS configuration object
        """
        self.config = config
        self.config.validate()

    def get_user_api(self):
        """
        Gets UserApi instance for user-related operations.

        Returns:
            UserApi instance
        """
        from chainup_custody_sdk.waas.api.user_api import UserApi

        return UserApi(self.config)

    def get_account_api(self):
        """
        Gets AccountApi instance for account-related operations.

        Returns:
            AccountApi instance
        """
        from chainup_custody_sdk.waas.api.account_api import AccountApi

        return AccountApi(self.config)

    def get_billing_api(self):
        """
        Gets BillingApi instance for billing and transaction operations.

        Returns:
            BillingApi instance
        """
        from chainup_custody_sdk.waas.api.billing_api import BillingApi

        return BillingApi(self.config)

    def get_coin_api(self):
        """
        Gets CoinApi instance for coin and blockchain operations.

        Returns:
            CoinApi instance
        """
        from chainup_custody_sdk.waas.api.coin_api import CoinApi

        return CoinApi(self.config)

    def get_transfer_api(self):
        """
        Gets TransferApi instance for transfer operations.

        Returns:
            TransferApi instance
        """
        from chainup_custody_sdk.waas.api.transfer_api import TransferApi

        return TransferApi(self.config)

    def get_async_notify_api(self):
        """
        Gets AsyncNotifyApi instance for async notification operations.

        Returns:
            AsyncNotifyApi instance
        """
        from chainup_custody_sdk.waas.api.async_notify_api import AsyncNotifyApi

        return AsyncNotifyApi(self.config)

    @staticmethod
    def new_builder():
        """
        Creates a new Builder instance for configuring WaasClient.

        Returns:
            Builder instance
        """
        return WaasClientBuilder()


class WaasClientBuilder:
    """
    Builder class for constructing WaasClient instances.
    Implements the Builder pattern for flexible configuration.
    """

    def __init__(self):
        """Creates a new Builder instance."""
        self.options = {}

    def set_host(self, host: str):
        """
        Sets the API host URL.

        Args:
            host: API host URL

        Returns:
            This builder instance for chaining
        """
        self.options["host"] = host
        return self

    def set_app_id(self, app_id: str):
        """
        Sets the application ID.

        Args:
            app_id: Application ID

        Returns:
            This builder instance for chaining
        """
        self.options["app_id"] = app_id
        return self

    def set_private_key(self, private_key: str):
        """
        Sets the RSA private key.

        Args:
            private_key: RSA private key

        Returns:
            This builder instance for chaining
        """
        self.options["private_key"] = private_key
        return self

    def set_public_key(self, public_key: str):
        """
        Sets the ChainUp public key.

        Args:
            public_key: ChainUp public key

        Returns:
            This builder instance for chaining
        """
        self.options["public_key"] = public_key
        return self

    def set_crypto_provider(self, crypto_provider: ICryptoProvider):
        """
        Sets a custom crypto provider for encryption/decryption.

        Args:
            crypto_provider: Custom crypto provider implementation

        Returns:
            This builder instance for chaining
        """
        self.options["crypto_provider"] = crypto_provider
        return self

    def set_version(self, version: str):
        """
        Sets the API version.

        Args:
            version: API version (default: 'v2')

        Returns:
            This builder instance for chaining
        """
        self.options["version"] = version
        return self

    def set_charset(self, charset: str):
        """
        Sets the charset encoding.

        Args:
            charset: Charset encoding (default: 'UTF-8')

        Returns:
            This builder instance for chaining
        """
        self.options["charset"] = charset
        return self

    def set_debug(self, debug: bool):
        """
        Enables or disables debug mode.

        Args:
            debug: Debug flag

        Returns:
            This builder instance for chaining
        """
        self.options["debug"] = debug
        return self

    def build(self) -> WaasClient:
        """
        Builds and returns a configured WaasClient instance.

        Returns:
            Configured WaasClient instance

        Raises:
            ValueError: If required configuration is missing
        """
        config = WaasConfig(**self.options)
        return WaasClient(config)
