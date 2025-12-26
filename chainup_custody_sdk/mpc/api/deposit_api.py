"""
Deposit API - MPC deposit management operations
"""
from typing import Dict, Any, List, Optional
from chainup_custody_sdk.mpc.api.mpc_base_api import MpcBaseApi


class DepositApi(MpcBaseApi):
    """
    Deposit API - MPC deposit management operations.
    Provides methods for querying deposit records.
    """

    def __init__(self, config):
        """
        Creates a new DepositApi instance.

        Args:
            config: MpcConfig object
        """
        super().__init__(config)

    def get_deposit_records(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gets receiving records.

        Args:
            params: Query parameters
                - ids: Receiving IDs (list of integers, up to 100)

        Returns:
            Deposit records

        Example:
            deposits = deposit_api.get_deposit_records({
                'ids': [123, 456, 789]
            })
        """
        if not params.get("ids") or not isinstance(params["ids"], list) or len(params["ids"]) == 0:
            raise ValueError('Parameter "ids" is required and must be a non-empty list')

        response = self.get(
            "/api/mpc/billing/deposit_list", {"ids": ",".join(map(str, params["ids"]))}
        )
        return self.validate_response(response)

    def sync_deposit_records(self, max_id: int = 0) -> Dict[str, Any]:
        """
        Synchronizes transfer(deposit) records.

        Args:
            max_id: Receiving record initial ID (default: 0)

        Returns:
            Synchronized deposit records

        Example:
            deposits = deposit_api.sync_deposit_records(0)
        """
        response = self.get(
            "/api/mpc/billing/sync_deposit_list", {"max_id": max_id}
        )
        return self.validate_response(response)
