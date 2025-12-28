"""
Wallet API - MPC wallet management operations
"""
from typing import Dict, Any, Optional
from chainup_custody_sdk.mpc.api.mpc_base_api import MpcBaseApi


class WalletApi(MpcBaseApi):
    """
    Wallet API - MPC wallet management operations.
    Provides methods for creating and managing MPC wallets.
    Uses snake_case naming for parameters (same as Java SDK).
    """

    def __init__(self, config):
        """
        Creates a new WalletApi instance.

        Args:
            config: MpcConfig object
        """
        super().__init__(config)

    def create_wallet(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new wallet.

        Args:
            params: Wallet creation parameters (snake_case naming)
                - sub_wallet_name: Wallet name (max 50 characters)
                - app_show_status: Display status: 1 (show), 2 (hide, default)

        Returns:
            Created wallet information with sub_wallet_id

        Example:
            wallet = wallet_api.create_wallet({
                'sub_wallet_name': 'My Wallet',
                'app_show_status': 1
            })
        """
        if not params.get("sub_wallet_name"):
            raise ValueError('Parameter "sub_wallet_name" is required')

        if len(params["sub_wallet_name"]) > 50:
            raise ValueError("Wallet name cannot be longer than 50 characters")

        response = self.post("/api/mpc/sub_wallet/create", params)
        return self.validate_response(response)

    def create_wallet_address(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a wallet address.

        Args:
            params: Address creation parameters (snake_case naming)
                - sub_wallet_id: Wallet ID
                - symbol: Unique identifier for the coin (e.g., "ETH")

        Returns:
            Created address information

        Example:
            address = wallet_api.create_wallet_address({
                'sub_wallet_id': 123,
                'symbol': 'ETH'
            })
        """
        if not params.get("sub_wallet_id"):
            raise ValueError('Parameter "sub_wallet_id" is required')

        if not params.get("symbol"):
            raise ValueError('Parameter "symbol" is required')

        response = self.post("/api/mpc/sub_wallet/create/address", params)
        return self.validate_response(response)

    def query_wallet_address(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Queries wallet address list.

        Args:
            params: Query parameters (snake_case naming)
                - sub_wallet_id: Wallet ID
                - symbol: Unique identifier for the coin (e.g., "ETH")
                - max_id: Starting address ID (optional, default: 0)

        Returns:
            Wallet address list

        Example:
            addresses = wallet_api.query_wallet_address({
                'sub_wallet_id': 123,
                'symbol': 'ETH',
                'max_id': 0
            })
        """
        if not params.get("sub_wallet_id"):
            raise ValueError('Parameter "sub_wallet_id" is required')

        if not params.get("symbol"):
            raise ValueError('Parameter "symbol" is required')

        response = self.post("/api/mpc/sub_wallet/get/address/list", params)
        return self.validate_response(response)

    def get_wallet_assets(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gets wallet assets.

        Args:
            params: Query parameters (snake_case naming)
                - sub_wallet_id: Wallet ID
                - symbol: Unique identifier for the coin (e.g., "ETH")

        Returns:
            Wallet asset information

        Example:
            assets = wallet_api.get_wallet_assets({
                'sub_wallet_id': 123,
                'symbol': 'ETH'
            })
        """
        if not params.get("sub_wallet_id"):
            raise ValueError('Parameter "sub_wallet_id" is required')

        if not params.get("symbol"):
            raise ValueError('Parameter "symbol" is required')

        response = self.get("/api/mpc/sub_wallet/assets", params)
        return self.validate_response(response)

    def change_wallet_show_status(self, params: Dict[str, Any]) -> bool:
        """
        Modifies the wallet display status.

        Args:
            params: Update parameters (snake_case naming)
                - sub_wallet_ids: Wallet IDs (comma-separated string, e.g., "123,456")
                - app_show_status: Display status: 1 (show), 2 (hide)

        Returns:
            True if successful

        Example:
            result = wallet_api.change_wallet_show_status({
                'sub_wallet_ids': '123,456',
                'app_show_status': 1
            })
        """
        if not params.get("sub_wallet_ids"):
            raise ValueError('Parameter "sub_wallet_ids" is required')

        if not params.get("app_show_status") or params["app_show_status"] not in [1, 2]:
            raise ValueError('Parameter "app_show_status" is required and must be 1 or 2')

        response = self.post("/api/mpc/sub_wallet/change_show_status", params)
        result = self.validate_response(response)
        return result.get("code") == "0"

    def wallet_address_info(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verifies address information.
        Input a specific address and get the response of the corresponding custody
        user and currency information.

        Args:
            params: Query parameters (snake_case naming)
                - address: Any address
                - memo: If it's a Memo type, input the memo (optional)

        Returns:
            Address information

        Example:
            info = wallet_api.wallet_address_info({
                'address': '0x123...',
                'memo': 'optional-memo'
            })
        """
        if not params.get("address"):
            raise ValueError('Parameter "address" is required')

        response = self.get("/api/mpc/sub_wallet/address/info", params)
        return self.validate_response(response)
