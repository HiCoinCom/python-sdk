"""
Auto Sweep API - MPC auto-sweep management operations
"""
from typing import Dict, Any, Optional
from chainup_custody_sdk.mpc.api.mpc_base_api import MpcBaseApi


class AutoSweepApi(MpcBaseApi):
    """
    Auto Sweep API - MPC auto-sweep management operations.
    Provides methods for configuring and querying auto-sweep operations.
    """

    def __init__(self, config):
        """
        Creates a new AutoSweepApi instance.

        Args:
            config: MpcConfig object
        """
        super().__init__(config)

    def auto_collect_sub_wallets(self, params: Dict[str, str]) -> Dict[str, Any]:
        """
        Gets auto-sweep wallets.
        Retrieve the auto-sweep wallet and auto fueling wallet for a specific coin.

        Args:
            params: Query parameters
                - symbol: Unique identifier for the coin (e.g., "USDTERC20")

        Returns:
            Auto-sweep wallet information

        Example:
            wallets = auto_sweep_api.auto_collect_sub_wallets({
                'symbol': 'USDTERC20'
            })
        """
        if not params.get("symbol"):
            raise ValueError('Parameter "symbol" is required')

        response = self.get(
            "/api/mpc/auto_collect/sub_wallets", {"symbol": params["symbol"]}
        )
        return self.validate_response(response)

    def set_auto_collect_symbol(self, params: Dict[str, str]) -> Dict[str, Any]:
        """
        Configures auto-sweep for coin.
        Set the minimum auto-sweep amount and the maximum miner fee for refueling.

        Args:
            params: Configuration parameters
                - symbol: Unique identifier for the coin (e.g., "USDTERC20")
                - collect_min: Minimum amount for auto-sweep (up to 6 decimal places)
                - fueling_limit: Maximum miner fee amount for auto-sweep (up to 6 decimal places)

        Returns:
            Configuration result

        Example:
            result = auto_sweep_api.set_auto_collect_symbol({
                'symbol': 'USDTERC20',
                'collect_min': '100',
                'fueling_limit': '0.01'
            })
        """
        required_fields = ["symbol", "collect_min", "fueling_limit"]
        for field in required_fields:
            if field not in params:
                raise ValueError(f"Required parameters: {', '.join(required_fields)}")

        response = self.post(
            "/api/mpc/auto_collect/symbol/set",
            {
                "symbol": params["symbol"],
                "collect_min": params["collect_min"],
                "fueling_limit": params["fueling_limit"],
            },
        )
        return self.validate_response(response)

    def sync_auto_collect_records(self, max_id: int = 0) -> Dict[str, Any]:
        """
        Synchronizes auto sweeping records.
        Retrieve up to 100 sweeping records for all wallets under a workspace.

        Args:
            max_id: Starting ID for sweeping records (default: 0)

        Returns:
            Synchronized auto-sweep records

        Example:
            records = auto_sweep_api.sync_auto_collect_records(0)
        """
        response = self.get(
            "/api/mpc/billing/sync_auto_collect_list",
            {"max_id": max_id},
        )
        return self.validate_response(response)
