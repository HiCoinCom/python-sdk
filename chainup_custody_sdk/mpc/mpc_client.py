"""
MPC Client - Main entry point for MPC API operations
Provides factory methods for creating MPC API instances
Uses Builder pattern for flexible configuration
"""
from typing import Optional
from chainup_custody_sdk.mpc.mpc_config import MpcConfig
from chainup_custody_sdk.utils.crypto_provider import ICryptoProvider


class MpcClient:
    """
    MPC Client - Main entry point for MPC API operations.
    Provides factory methods for creating MPC API instances.
    """

    def __init__(self, config: MpcConfig):
        """
        Private constructor - use Builder to create instances.

        Args:
            config: MPC configuration object
        """
        self.config = config
        self.config.validate()

    def get_wallet_api(self):
        """
        Gets WalletApi instance for wallet operations.

        Returns:
            WalletApi instance
        """
        from chainup_custody_sdk.mpc.api.wallet_api import WalletApi

        return WalletApi(self.config)

    def get_deposit_api(self):
        """
        Gets DepositApi instance for deposit operations.

        Returns:
            DepositApi instance
        """
        from chainup_custody_sdk.mpc.api.deposit_api import DepositApi

        return DepositApi(self.config)

    def get_withdraw_api(self):
        """
        Gets WithdrawApi instance for withdrawal operations.

        Returns:
            WithdrawApi instance
        """
        from chainup_custody_sdk.mpc.api.withdraw_api import WithdrawApi

        return WithdrawApi(self.config)

    def get_web3_api(self):
        """
        Gets Web3Api instance for Web3 operations.

        Returns:
            Web3Api instance
        """
        from chainup_custody_sdk.mpc.api.web3_api import Web3Api

        return Web3Api(self.config)

    def get_auto_sweep_api(self):
        """
        Gets AutoSweepApi instance for auto-sweep operations.

        Returns:
            AutoSweepApi instance
        """
        from chainup_custody_sdk.mpc.api.auto_sweep_api import AutoSweepApi

        return AutoSweepApi(self.config)

    def get_notify_api(self):
        """
        Gets NotifyApi instance for notification operations.

        Returns:
            NotifyApi instance
        """
        from chainup_custody_sdk.mpc.api.notify_api import NotifyApi

        return NotifyApi(self.config)

    def get_workspace_api(self):
        """
        Gets WorkSpaceApi instance for workspace operations.

        Returns:
            WorkSpaceApi instance
        """
        from chainup_custody_sdk.mpc.api.workspace_api import WorkSpaceApi

        return WorkSpaceApi(self.config)

    def get_tron_resource_api(self):
        """
        Gets TronResourceApi instance for TRON resource operations.

        Returns:
            TronResourceApi instance
        """
        from chainup_custody_sdk.mpc.api.tron_resource_api import TronResourceApi

        return TronResourceApi(self.config)

    @staticmethod
    def new_builder():
        """
        Creates a new Builder instance for configuring MpcClient.

        Returns:
            Builder instance
        """
        return MpcClientBuilder()


class MpcClientBuilder:
    """
    Builder class for constructing MpcClient instances.
    Implements the Builder pattern for flexible configuration.
    """

    def __init__(self):
        """Creates a new Builder instance."""
        self.options = {}

    def set_domain(self, domain: str):
        """
        Sets the API domain URL.

        Args:
            domain: API domain URL

        Returns:
            This builder instance for chaining
        """
        self.options["domain"] = domain
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

    def set_rsa_private_key(self, rsa_private_key: str):
        """
        Sets the RSA private key.

        Args:
            rsa_private_key: RSA private key

        Returns:
            This builder instance for chaining
        """
        self.options["rsa_private_key"] = rsa_private_key
        return self

    def set_waas_public_key(self, waas_public_key: str):
        """
        Sets the WaaS server public key for response decryption.

        Args:
            waas_public_key: WaaS server public key

        Returns:
            This builder instance for chaining
        """
        self.options["waas_public_key"] = waas_public_key
        return self

    def set_api_key(self, api_key: str):
        """
        Sets the API key.

        Args:
            api_key: API key for authentication

        Returns:
            This builder instance for chaining
        """
        self.options["api_key"] = api_key
        return self

    def set_sign_private_key(self, sign_private_key: str):
        """
        Sets the signing private key for withdrawal/Web3 transaction signatures.

        Args:
            sign_private_key: RSA private key for transaction signing (optional)

        Returns:
            This builder instance for chaining
        """
        self.options["sign_private_key"] = sign_private_key
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

    def build(self) -> MpcClient:
        """
        Builds and returns a configured MpcClient instance.

        Returns:
            Configured MpcClient instance

        Raises:
            ValueError: If required configuration is missing
        """
        config = MpcConfig(**self.options)
        return MpcClient(config)
