"""
Tron Resource API - TRON resource delegation operations
"""
from typing import Dict, Any, List
from chainup_custody_sdk.mpc.api.mpc_base_api import MpcBaseApi


class TronResourceApi(MpcBaseApi):
    """
    Tron Resource API - TRON resource delegation operations.
    Provides methods for buying and querying TRON network resources (Energy/Bandwidth).
    """

    def __init__(self, config):
        """
        Creates a new TronResourceApi instance.

        Args:
            config: MpcConfig object
        """
        super().__init__(config)

    def create_tron_delegate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates delegate (Buy Tron Resource).
        Purchase TRON network energy or bandwidth for a specific address.

        Args:
            params: Delegation parameters
                - request_id: Unique request ID (required)
                - buy_type: Buy type (optional)
                - resource_type: Resource type: 0 for energy, 1 for bandwidth (optional)
                - service_charge_type: Service charge type (required)
                - energy_num: Energy amount to purchase (optional)
                - net_num: Bandwidth amount to purchase (optional)
                - address_from: Address paying for resources (required)
                - address_to: Address to receive resources (optional)
                - contract_address: Contract address (optional)

        Returns:
            Delegation result with trans_id

        Example:
            result = tron_resource_api.create_tron_delegate({
                'request_id': 'unique-id',
                'resource_type': 0,
                'buy_type': 0,
                'address_from': 'TXxxx...',
                'address_to': 'TRxxx...',
                'contract_address': 'TEDxxx...',
                'service_charge_type': '10010'
            })
        """
        # Validate required parameters
        if not params.get("request_id"):
            raise ValueError("Required parameter: request_id")
        if not params.get("address_from"):
            raise ValueError("Required parameter: address_from")
        if not params.get("service_charge_type"):
            raise ValueError("Required parameter: service_charge_type")

        # Additional validation for buy_type 0 or 2
        buy_type = params.get("buy_type")
        if buy_type == 0 or buy_type == 2:
            if not params.get("address_to") or not params.get("contract_address"):
                raise ValueError(
                    "For buy_type 0 or 2, address_to and contract_address are required"
                )

        response = self.post("/api/mpc/tron/delegate", params)
        return self.validate_response(response)

    def get_buy_resource_records(self, request_ids: List[str]) -> Dict[str, Any]:
        """
        Gets buy resource records.
        Get delegation records by request IDs.

        Args:
            request_ids: Request IDs array (up to 100)

        Returns:
            Delegation records

        Example:
            records = tron_resource_api.get_buy_resource_records(['req-1', 'req-2'])
        """
        if not request_ids or not isinstance(request_ids, list) or len(request_ids) == 0:
            raise ValueError(
                'Parameter "request_ids" is required and must be a non-empty list'
            )

        # Java SDK uses "ids" parameter with comma-separated string
        response = self.post(
            "/api/mpc/tron/delegate/trans_list", {"ids": ",".join(request_ids)}
        )
        return self.validate_response(response)

    def sync_buy_resource_records(self, max_id: int = 0) -> Dict[str, Any]:
        """
        Synchronizes buy resource records.
        Get all delegation records, maximum of 100 records.

        Args:
            max_id: Starting ID of delegation records (default: 0)

        Returns:
            Synchronized delegation records

        Example:
            records = tron_resource_api.sync_buy_resource_records(0)
        """
        response = self.post(
            "/api/mpc/tron/delegate/sync_trans_list", {"max_id": max_id or 0}
        )
        return self.validate_response(response)
