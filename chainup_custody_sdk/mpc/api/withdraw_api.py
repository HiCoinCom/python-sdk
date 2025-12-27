"""
Withdraw API - MPC withdrawal management operations
"""
from typing import Dict, Any, List, Optional
from chainup_custody_sdk.mpc.api.mpc_base_api import MpcBaseApi
from chainup_custody_sdk.utils.mpc_sign_util import MpcSignUtil


class WithdrawApi(MpcBaseApi):
    """
    Withdraw API - MPC withdrawal management operations.
    Provides methods for initiating withdrawals and querying withdrawal records.
    """

    def __init__(self, config):
        """
        Creates a new WithdrawApi instance.

        Args:
            config: MpcConfig object
        """
        super().__init__(config)

    def withdraw(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Initiates a transfer (withdrawal).

        Args:
            params: Withdrawal parameters
                - request_id: Unique request ID
                - sub_wallet_id: Sub-wallet ID
                - symbol: Coin symbol (e.g., "USDTERC20")
                - amount: Withdrawal amount
                - address_to: Destination address
                - from: Specify the transfer coin address (optional)
                - memo: Address memo (for coins that require it) (optional)
                - remark: Withdrawal remark (optional)
                - outputs: UTXO outputs (for BTC-like coins) (optional)
                - need_transaction_sign: Whether to sign the transaction (optional, default: False)

        Returns:
            Withdrawal result with withdraw_id

        Example:
            result = withdraw_api.withdraw({
                'request_id': 'unique-id',
                'sub_wallet_id': 123,
                'symbol': 'ETH',
                'amount': '0.1',
                'address_to': '0x123...'
            })
        """
        required_fields = ["request_id", "sub_wallet_id", "symbol", "amount", "address_to"]
        for field in required_fields:
            if not params.get(field):
                raise ValueError(
                    f"Required parameters: {', '.join(required_fields)}"
                )

        need_transaction_sign = params.get("need_transaction_sign", False)

        # Check if sign_private_key or crypto_provider is configured when signature is required
        if need_transaction_sign and not self.config.sign_private_key and not self.config.crypto_provider:
            raise ValueError(
                "MPC withdrawal requires sign_private_key in config or crypto_provider when need_transaction_sign is True"
            )

        request_data = {
            "request_id": params["request_id"],
            "sub_wallet_id": params["sub_wallet_id"],
            "symbol": params["symbol"],
            "amount": params["amount"],
            "address_to": params["address_to"],
        }

        # Add optional fields
        if params.get("from"):
            request_data["from"] = params["from"]
        if params.get("memo"):
            request_data["memo"] = params["memo"]
        if params.get("remark"):
            request_data["remark"] = params["remark"]
        if params.get("outputs"):
            request_data["outputs"] = params["outputs"]

        # Generate signature if needed
        if need_transaction_sign:
            try:
                sign_params = {
                    "request_id": params["request_id"],
                    "sub_wallet_id": params["sub_wallet_id"],
                    "symbol": params["symbol"],
                    "address_to": params["address_to"],
                    "amount": params["amount"],
                    "memo": params.get("memo"),
                    "outputs": params.get("outputs"),
                }
                
                # Use crypto_provider if available, otherwise fall back to sign_private_key
                if self.crypto_provider:
                    signature = MpcSignUtil.generate_withdraw_sign(
                        sign_params,
                        self.crypto_provider,
                    )
                else:
                    signature = MpcSignUtil.generate_withdraw_sign(
                        sign_params,
                        self.config.sign_private_key,
                    )
                
                if signature:
                    request_data["sign"] = signature
                else:
                    raise ValueError("Failed to generate transaction signature")
                    
            except Exception as e:
                raise RuntimeError(f"Transaction signing failed: {str(e)}")

        response = self.post("/api/mpc/billing/withdraw", request_data)
        return self.validate_response(response)

    def get_withdraw_records(self, request_ids: list) -> Dict[str, Any]:
        """
        Gets transfer records.

        Args:
            request_ids: Request IDs (list of strings, up to 100)

        Returns:
            Withdrawal records

        Example:
            records = withdraw_api.get_withdraw_records(['req-1', 'req-2'])
        """
        if not request_ids or not isinstance(request_ids, list) or len(request_ids) == 0:
            raise ValueError(
                'Parameter "request_ids" is required and must be a non-empty list'
            )

        response = self.get(
            "/api/mpc/billing/withdraw_list", {"ids": ",".join(request_ids)}
        )
        return self.validate_response(response)

    def sync_withdraw_records(self, max_id: int = 0) -> Dict[str, Any]:
        """
        Synchronizes transfer(withdraw) records.

        Args:
            max_id: Starting ID of withdraw records (default: 0)

        Returns:
            Synchronized withdrawal records

        Example:
            records = withdraw_api.sync_withdraw_records(0)
        """
        response = self.get(
            "/api/mpc/billing/sync_withdraw_list", {"max_id": max_id}
        )
        return self.validate_response(response)
