"""
Coin API - Cryptocurrency information operations
"""
from typing import Dict, Any, List, Optional
from chainup_custody_sdk.waas.api.base_api import BaseApi


class CoinApi(BaseApi):
    """
    Coin API - Cryptocurrency information operations.
    Provides methods for querying supported cryptocurrencies.
    """

    def __init__(self, config):
        """
        Creates a new CoinApi instance.

        Args:
            config: WaasConfig object
        """
        super().__init__(config)

    def get_coin_list(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Gets supported coin list.
        Retrieves information about all cryptocurrencies supported by the platform.

        Args:
            params: Optional parameters

        Returns:
            List of supported coins with details including:
            - symbol: Coin symbol
            - icon: Icon URL
            - real_symbol: Real symbol
            - base_symbol: Base chain symbol
            - decimals: Decimal places
            - contract_address: Token contract address (if applicable)
            - deposit_confirmation: Required confirmations for deposit
            - support_memo: Whether memo/tag is supported
            - support_token: Whether tokens are supported
            - address_regex: Address validation regex
            - address_tag_regex: Memo/tag validation regex
            - min_deposit: Minimum deposit amount

        Example:
            coin_list = coin_api.get_coin_list()
        """
        params = params or {}
        response = self.post("/user/getCoinList", params)
        return self.validate_response(response)
