"""
MPC Client - Main entry point for MPC API operations
Provides factory methods for creating MPC API instances
Uses Builder pattern for flexible configuration
"""
from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from chainup_custody_sdk.mpc.mpc_config import MpcConfig
from chainup_custody_sdk.logger import get_logger, LoggerMixin

if TYPE_CHECKING:
    from chainup_custody_sdk.utils.crypto_provider import ICryptoProvider
    from chainup_custody_sdk.mpc.api.wallet_api import WalletApi
    from chainup_custody_sdk.mpc.api.deposit_api import DepositApi
    from chainup_custody_sdk.mpc.api.withdraw_api import WithdrawApi
    from chainup_custody_sdk.mpc.api.web3_api import Web3Api
    from chainup_custody_sdk.mpc.api.auto_sweep_api import AutoSweepApi
    from chainup_custody_sdk.mpc.api.notify_api import NotifyApi
    from chainup_custody_sdk.mpc.api.workspace_api import WorkSpaceApi
    from chainup_custody_sdk.mpc.api.tron_resource_api import TronResourceApi


class MpcClient(LoggerMixin):
    """
    MPC Client - Main entry point for MPC API operations.
    
    Provides factory methods for creating MPC API instances.
    Supports context manager protocol for resource management.
    
    Example:
        # Using builder pattern
        client = (
            MpcClient.builder()
            .set_app_id("your-app-id")
            .set_rsa_private_key("your-private-key")
            .build()
        )
        
        # Using context manager
        with MpcClient.builder().set_app_id("...").build() as client:
            wallet_api = client.get_wallet_api()
            # ... use API
    """
    
    __slots__ = ("config", "_closed")

    def __init__(self, config: MpcConfig) -> None:
        """
        Creates a new MpcClient instance.
        
        Args:
            config: MPC configuration object
        
        Note:
            Prefer using MpcClient.builder() for construction.
        """
        self.config = config
        self._closed = False
        self.config.validate()
        self._logger.debug(f"MpcClient initialized with app_id={config.app_id}")

    def __enter__(self) -> "MpcClient":
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
            self._logger.debug("MpcClient closed")

    def get_wallet_api(self) -> "WalletApi":
        """
        Gets WalletApi instance for wallet operations.

        Returns:
            WalletApi instance
        """
        from chainup_custody_sdk.mpc.api.wallet_api import WalletApi
        return WalletApi(self.config)

    def get_deposit_api(self) -> "DepositApi":
        """
        Gets DepositApi instance for deposit operations.

        Returns:
            DepositApi instance
        """
        from chainup_custody_sdk.mpc.api.deposit_api import DepositApi
        return DepositApi(self.config)

    def get_withdraw_api(self) -> "WithdrawApi":
        """
        Gets WithdrawApi instance for withdrawal operations.

        Returns:
            WithdrawApi instance
        """
        from chainup_custody_sdk.mpc.api.withdraw_api import WithdrawApi
        return WithdrawApi(self.config)

    def get_web3_api(self) -> "Web3Api":
        """
        Gets Web3Api instance for Web3 operations.

        Returns:
            Web3Api instance
        """
        from chainup_custody_sdk.mpc.api.web3_api import Web3Api
        return Web3Api(self.config)

    def get_auto_sweep_api(self) -> "AutoSweepApi":
        """
        Gets AutoSweepApi instance for auto-sweep operations.

        Returns:
            AutoSweepApi instance
        """
        from chainup_custody_sdk.mpc.api.auto_sweep_api import AutoSweepApi
        return AutoSweepApi(self.config)

    def get_notify_api(self) -> "NotifyApi":
        """
        Gets NotifyApi instance for notification operations.

        Returns:
            NotifyApi instance
        """
        from chainup_custody_sdk.mpc.api.notify_api import NotifyApi
        return NotifyApi(self.config)

    def get_workspace_api(self) -> "WorkSpaceApi":
        """
        Gets WorkSpaceApi instance for workspace operations.

        Returns:
            WorkSpaceApi instance
        """
        from chainup_custody_sdk.mpc.api.workspace_api import WorkSpaceApi
        return WorkSpaceApi(self.config)

    def get_tron_resource_api(self) -> "TronResourceApi":
        """
        Gets TronResourceApi instance for TRON resource operations.

        Returns:
            TronResourceApi instance
        """
        from chainup_custody_sdk.mpc.api.tron_resource_api import TronResourceApi
        return TronResourceApi(self.config)

    @staticmethod
    def builder() -> "MpcClientBuilder":
        """
        Creates a new Builder instance for configuring MpcClient.

        Returns:
            Builder instance
        
        Example:
            client = MpcClient.builder().set_app_id("...").build()
        """
        return MpcClientBuilder()
    
    @staticmethod
    def new_builder() -> "MpcClientBuilder":
        """
        Creates a new Builder instance (alias for builder()).
        
        Returns:
            Builder instance
        """
        return MpcClientBuilder()


class MpcClientBuilder:
    """
    Builder class for constructing MpcClient instances.
    
    Implements the Builder pattern for flexible configuration.
    All setter methods return self for method chaining.
    
    Example:
        client = (
            MpcClientBuilder()
            .set_app_id("your-app-id")
            .set_rsa_private_key("your-private-key")
            .set_waas_public_key("waas-public-key")
            .set_debug(True)
            .build()
        )
    """
    
    __slots__ = ("_options",)

    def __init__(self) -> None:
        """Creates a new Builder instance."""
        self._options: dict = {}

    def set_domain(self, domain: str) -> "MpcClientBuilder":
        """
        Sets the API domain URL.

        Args:
            domain: API domain URL

        Returns:
            This builder instance for chaining
        """
        self._options["domain"] = domain
        return self

    def set_app_id(self, app_id: str) -> "MpcClientBuilder":
        """
        Sets the application ID.

        Args:
            app_id: Application ID

        Returns:
            This builder instance for chaining
        """
        self._options["app_id"] = app_id
        return self

    def set_rsa_private_key(self, rsa_private_key: str) -> "MpcClientBuilder":
        """
        Sets the RSA private key.

        Args:
            rsa_private_key: RSA private key

        Returns:
            This builder instance for chaining
        """
        self._options["rsa_private_key"] = rsa_private_key
        return self

    def set_waas_public_key(self, waas_public_key: str) -> "MpcClientBuilder":
        """
        Sets the WaaS server public key for response decryption.

        Args:
            waas_public_key: WaaS server public key

        Returns:
            This builder instance for chaining
        """
        self._options["waas_public_key"] = waas_public_key
        return self

    def set_api_key(self, api_key: str) -> "MpcClientBuilder":
        """
        Sets the API key.

        Args:
            api_key: API key for authentication

        Returns:
            This builder instance for chaining
        """
        self._options["api_key"] = api_key
        return self

    def set_sign_private_key(self, sign_private_key: str) -> "MpcClientBuilder":
        """
        Sets the signing private key for withdrawal/Web3 transaction signatures.

        Args:
            sign_private_key: RSA private key for transaction signing (optional)

        Returns:
            This builder instance for chaining
        """
        self._options["sign_private_key"] = sign_private_key
        return self

    def set_crypto_provider(self, crypto_provider: "ICryptoProvider") -> "MpcClientBuilder":
        """
        Sets a custom crypto provider for encryption/decryption.

        Args:
            crypto_provider: Custom crypto provider implementation

        Returns:
            This builder instance for chaining
        """
        self._options["crypto_provider"] = crypto_provider
        return self

    def set_debug(self, debug: bool) -> "MpcClientBuilder":
        """
        Enables or disables debug mode.

        Args:
            debug: Debug flag

        Returns:
            This builder instance for chaining
        """
        self._options["debug"] = debug
        return self

    def build(self) -> MpcClient:
        """
        Builds and returns a configured MpcClient instance.

        Returns:
            Configured MpcClient instance

        Raises:
            ConfigError: If required configuration is missing
        """
        config = MpcConfig(**self._options)
        return MpcClient(config)
