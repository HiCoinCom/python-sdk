"""
Billing API - Deposit, withdrawal and miner fee operations
"""
from typing import Dict, Any, List, Optional
from chainup_custody_sdk.waas.api.base_api import BaseApi


class BillingApi(BaseApi):
    """
    Billing API - Deposit, withdrawal and miner fee operations.
    Provides methods for withdraw requests and querying deposit/withdrawal records.
    """

    def __init__(self, config):
        """
        Creates a new BillingApi instance.

        Args:
            config: WaasConfig object
        """
        super().__init__(config)

    def withdraw(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a withdrawal request.

        Args:
            params: Withdrawal parameters
                - request_id: Unique request ID (merchant generated)
                - from_uid: Source user ID
                - to_address: Destination address or (address_memo for XRP)
                - amount: Withdrawal amount
                - symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')

        Returns:
            Withdrawal result

        Example:
            result = billing_api.withdraw({
                'request_id': 'withdraw_001',
                'from_uid': 12345,
                'to_address': '0x1234...',
                'amount': '1.5',
                'symbol': 'ETH'
            })
        """
        response = self.post("/billing/withdraw", params)
        return self.validate_response(response)

    def withdraw_list(self, ids: list) -> List[Dict[str, Any]]:
        """
        Gets withdrawal records by request IDs.

        Args:
            ids: List of request IDs

        Returns:
            Withdrawal records

        Example:
            withdrawals = billing_api.withdraw_list(['withdraw_001', 'withdraw_002'])
        """
        response = self.post("/billing/withdrawList", {"ids": ",".join(ids)})
        return self.validate_response(response)

    def sync_withdraw_list(self, max_id: int = 0) -> List[Dict[str, Any]]:
        """
        Syncs withdrawal records by max ID (pagination).

        Args:
            max_id: Maximum transaction ID for pagination

        Returns:
            Synced withdrawal records

        Example:
            withdrawals = billing_api.sync_withdraw_list(0)
        """
        response = self.post("/billing/syncWithdrawList", {"max_id": max_id})
        return self.validate_response(response)

    def deposit_list(self, ids: list) -> List[Dict[str, Any]]:
        """
        Gets deposit records by WaaS IDs.

        Args:
            ids: List of WaaS deposit IDs

        Returns:
            Deposit records

        Example:
            deposits = billing_api.deposit_list(['123', '456'])
        """
        response = self.post("/billing/depositList", {"ids": ",".join(ids)})
        return self.validate_response(response)

    def sync_deposit_list(self, max_id: int = 0) -> List[Dict[str, Any]]:
        """
        Syncs deposit records by max ID (pagination).

        Args:
            max_id: Maximum transaction ID for pagination

        Returns:
            Synced deposit records

        Example:
            deposits = billing_api.sync_deposit_list(0)
        """
        response = self.post("/billing/syncDepositList", {"max_id": max_id})
        return self.validate_response(response)

    def miner_fee_list(self, ids: list) -> List[Dict[str, Any]]:
        """
        Gets miner fee records by WaaS IDs.

        Args:
            ids: List of WaaS transaction IDs

        Returns:
            Miner fee records

        Example:
            fees = billing_api.miner_fee_list(['123', '456'])
        """
        response = self.post("/billing/minerFeeList", {"ids": ",".join(ids)})
        return self.validate_response(response)

    def sync_miner_fee_list(self, max_id: int = 0) -> List[Dict[str, Any]]:
        """
        Syncs miner fee records by max ID (pagination).

        Args:
            max_id: Maximum transaction ID for pagination

        Returns:
            Synced miner fee records

        Example:
            fees = billing_api.sync_miner_fee_list(0)
        """
        response = self.post("/billing/syncMinerFeeList", {"max_id": max_id})
        return self.validate_response(response)
