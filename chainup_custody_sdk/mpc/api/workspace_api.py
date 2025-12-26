"""
WorkSpace API - MPC workspace management operations
"""
from typing import Dict, Any, Optional
from chainup_custody_sdk.mpc.api.mpc_base_api import MpcBaseApi


class WorkSpaceApi(MpcBaseApi):
    """
    WorkSpace API - MPC workspace management operations.
    Provides methods for querying supported chains, coins, and blockchain information.
    """

    def __init__(self, config):
        """
        Creates a new WorkSpaceApi instance.

        Args:
            config: MpcConfig object
        """
        super().__init__(config)

    def get_support_main_chain(self) -> Dict[str, Any]:
        """
        Gets supported main chains.
        Get the supported MPC main chain coins and the MPC main chain coins opened in ChainUp Custody.

        Returns:
            Supported main chains

        Example:
            chains = workspace_api.get_support_main_chain()
        """
        response = self.get("/api/mpc/wallet/open_coin", {})
        return self.validate_response(response)

    def get_coin_details(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Gets MPC workspace coin details.
        Get the details of MPC workspace's main chain coins and tokens supported.

        Args:
            params: Query parameters (optional, using snake_case naming)
                - symbol: Unique identifier for the coin (e.g., "USDTERC20")
                - base_symbol: Main chain coin symbol (e.g., "ETH")
                - open_chain: True: opened coins, False: unopened coins
                - max_id: Starting ID of the currency
                - limit: Number of currencies to get (default: 1500)

        Returns:
            Coin details

        Example:
            coins = workspace_api.get_coin_details({
                'base_symbol': 'ETH',
                'open_chain': True,
                'limit': 100
            })
        """
        params = params or {}
        # Pass params directly using snake_case (same as Java SDK)
        response = self.get("/api/mpc/coin_list", params)
        return self.validate_response(response)

    def get_last_block_height(self, params: Dict[str, str]) -> Dict[str, Any]:
        """
        Gets last block height.
        Get the latest block height of the specified main chain.

        Args:
            params: Query parameters (using snake_case naming)
                - base_symbol: Main chain coin symbol (e.g., "ETH", "BTC")

        Returns:
            Block height information

        Example:
            block_info = workspace_api.get_last_block_height({
                'base_symbol': 'ETH'
            })
        """
        if not params.get("base_symbol"):
            raise ValueError('Parameter "base_symbol" is required')

        # Pass params directly using snake_case (same as Java SDK)
        response = self.get("/api/mpc/chain_height", params)
        return self.validate_response(response)
