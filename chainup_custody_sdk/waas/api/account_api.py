"""
Account API - Account and balance management operations
"""
from typing import Dict, Any, List
from chainup_custody_sdk.waas.api.base_api import BaseApi


class AccountApi(BaseApi):
    """
    Account API - Account and balance management operations.
    Provides methods for querying account balances and deposit addresses.
    """

    def __init__(self, config):
        """
        Creates a new AccountApi instance.

        Args:
            config: WaasConfig object
        """
        super().__init__(config)

    def get_user_account(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gets user account balance for a specific cryptocurrency.

        Args:
            params: Query parameters
                - uid: User ID
                - symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')

        Returns:
            Account balance information

        Example:
            account = account_api.get_user_account({
                'uid': 12345,
                'symbol': 'BTC'
            })
        """
        response = self.post("/account/getByUidAndSymbol", params)
        return self.validate_response(response)

    def get_user_address(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gets user deposit address for a specific cryptocurrency.

        Args:
            params: Query parameters
                - uid: User ID
                - symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')

        Returns:
            Deposit address information

        Example:
            address = account_api.get_user_address({
                'uid': 12345,
                'symbol': 'ETH'
            })
        """
        response = self.post("/account/getDepositAddress", params)
        return self.validate_response(response)

    def get_company_account(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gets company (merchant) account balance for a specific cryptocurrency.

        Args:
            params: Query parameters
                - symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')

        Returns:
            Company account information

        Example:
            account = account_api.get_company_account({'symbol': 'ETH'})
        """
        response = self.post("/account/getCompanyBySymbol", params)
        return self.validate_response(response)

    def get_user_address_info(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gets user address information by address.

        Args:
            params: Query parameters
                - address: Blockchain address to query

        Returns:
            Address details

        Example:
            info = account_api.get_user_address_info({'address': '0x1234...'})
        """
        response = self.post("/account/getDepositAddressInfo", params)
        return self.validate_response(response)

    def sync_user_address_list(self, max_id: int = 0) -> List[Dict[str, Any]]:
        """
        Syncs user address list by max ID (pagination).

        Args:
            max_id: Maximum address ID for pagination (0 for first sync)

        Returns:
            Synced user address list with id, uid, address, symbol

        Example:
            addresses = account_api.sync_user_address_list(0)
        """
        response = self.post("/address/syncList", {"max_id": max_id})
        return self.validate_response(response)
