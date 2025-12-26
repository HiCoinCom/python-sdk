"""
Transfer API - Internal account transfer operations
"""
from typing import Dict, Any, List
from chainup_custody_sdk.waas.api.base_api import BaseApi


class TransferApi(BaseApi):
    """
    Transfer API - Internal account transfer operations.
    Provides methods for transferring funds between merchant accounts.
    """

    # Query type constants
    REQUEST_ID = "request_id"
    RECEIPT = "receipt"

    def __init__(self, config):
        """
        Creates a new TransferApi instance.

        Args:
            config: WaasConfig object
        """
        super().__init__(config)

    def account_transfer(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Internal transfer between merchant accounts.

        Args:
            params: Transfer parameters
                - request_id: Unique request ID (merchant generated)
                - symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
                - amount: Transfer amount
                - from: Source user ID (as string)
                - to: Destination user ID (as string)
                - remark (optional): Transfer remark

        Returns:
            Transfer result

        Example:
            result = transfer_api.account_transfer({
                'request_id': 'transfer_001',
                'symbol': 'USDT',
                'amount': '100.5',
                'from': '123',
                'to': '456',
                'remark': 'Internal transfer'
            })
        """
        response = self.post("/account/transfer", params)
        return self.validate_response(response)

    def get_account_transfer_list(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Gets transfer records by request IDs or receipts.

        Args:
            params: Query parameters
                - ids: Comma-separated list of IDs to query
                - ids_type: Type of IDs: TransferApi.REQUEST_ID or TransferApi.RECEIPT

        Returns:
            Transfer records

        Example:
            transfers = transfer_api.get_account_transfer_list({
                'ids': 'transfer_001,transfer_002',
                'ids_type': TransferApi.REQUEST_ID
            })
        """
        response = self.post("/account/transferList", params)
        return self.validate_response(response)

    def sync_account_transfer_list(self, max_id: int = 0) -> List[Dict[str, Any]]:
        """
        Syncs transfer records by max ID (pagination).

        Args:
            max_id: Maximum transaction ID for pagination

        Returns:
            Synced transfer records

        Example:
            transfers = transfer_api.sync_account_transfer_list(0)
        """
        response = self.post("/account/syncTransferList", {"max_id": max_id})
        return self.validate_response(response)
