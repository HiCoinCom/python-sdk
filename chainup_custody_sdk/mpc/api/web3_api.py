"""
Web3 API - MPC Web3 transaction operations
"""
from typing import Dict, Any, Optional
from chainup_custody_sdk.mpc.api.mpc_base_api import MpcBaseApi
from chainup_custody_sdk.utils.mpc_sign_util import MpcSignUtil


class Web3Api(MpcBaseApi):
    """
    Web3 API - MPC Web3 transaction operations.
    Provides methods for creating, accelerating, and querying Web3 transactions.
    """

    def __init__(self, config):
        """
        Creates a new Web3Api instance.

        Args:
            config: MpcConfig object
        """
        super().__init__(config)

    def create_web3_trans(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a Web3 transaction.

        Args:
            params: Transaction parameters
                - request_id: Unique request ID (required)
                - sub_wallet_id: Sub-wallet ID (required)
                - main_chain_symbol: Main chain coin symbol, e.g. ETH (required)
                - interactive_contract: Interactive contract address (required)
                - amount: Transfer amount (required)
                - gas_price: Gas price in Gwei (required)
                - gas_limit: Gas limit (required)
                - input_data: Hexadecimal data for contract transaction (required)
                - trans_type: Transaction type: 0=Authorization, 1=Other (required)
                - from: Transaction initiation address (optional)
                - dapp_name: Dapp name (optional)
                - dapp_url: Dapp URL (optional)
                - dapp_img: Dapp image (optional)
                - need_transaction_sign: Whether transaction signature is required (optional, default: False)

        Returns:
            Created transaction result

        Example:
            result = web3_api.create_web3_trans({
                'request_id': 'unique-id',
                'sub_wallet_id': 123,
                'main_chain_symbol': 'ETH',
                'interactive_contract': '0x123...',
                'amount': '1000000000000000000',
                'gas_price': '20',
                'gas_limit': '21000',
                'input_data': '0x',
                'trans_type': '1'
            })
        """
        required_fields = [
            "request_id",
            "sub_wallet_id",
            "main_chain_symbol",
            "interactive_contract",
            "amount",
            "gas_price",
            "gas_limit",
            "input_data",
            "trans_type",
        ]
        for field in required_fields:
            if field not in params:
                raise ValueError(f"Required parameters: {', '.join(required_fields)}")

        need_transaction_sign = params.get("need_transaction_sign", False)

        # Check if sign_private_key is configured when signature is required
        if need_transaction_sign and not self.config.sign_private_key:
            raise ValueError(
                "MPC web3 transaction requires sign_private_key in config when need_transaction_sign is True"
            )

        request_data = {
            "request_id": params["request_id"],
            "sub_wallet_id": params["sub_wallet_id"],
            "main_chain_symbol": params["main_chain_symbol"],
            "interactive_contract": params["interactive_contract"],
            "amount": params["amount"],
            "gas_price": params["gas_price"],
            "gas_limit": params["gas_limit"],
            "input_data": params["input_data"],
            "trans_type": params["trans_type"],
        }

        # Add optional parameters
        if params.get("from"):
            request_data["from"] = params["from"]
        if params.get("dapp_name"):
            request_data["dapp_name"] = params["dapp_name"]
        if params.get("dapp_url"):
            request_data["dapp_url"] = params["dapp_url"]
        if params.get("dapp_img"):
            request_data["dapp_img"] = params["dapp_img"]

        # Generate signature if needed
        if need_transaction_sign:
            try:
                signature = MpcSignUtil.generate_web3_sign(
                    {
                        "request_id": params["request_id"],
                        "sub_wallet_id": str(params["sub_wallet_id"]),
                        "main_chain_symbol": params["main_chain_symbol"],
                        "interactive_contract": params["interactive_contract"],
                        "amount": params["amount"],
                        "input_data": params["input_data"],
                    },
                    self.config.sign_private_key,
                )

                if signature:
                    request_data["sign"] = signature
                else:
                    raise ValueError("Failed to generate Web3 transaction signature")

            except Exception as e:
                raise RuntimeError(f"Web3 transaction signing failed: {str(e)}")

        response = self.post("/api/mpc/web3/trans/create", request_data)
        return self.validate_response(response)

    def accelerate_web3_trans(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Accelerates a Web3 transaction.

        Args:
            params: Acceleration parameters
                - request_id: Request ID to accelerate (required)
                - gas_price: New gas price in Gwei (required)
                - gas_limit: New gas limit (required)

        Returns:
            Acceleration result

        Example:
            result = web3_api.accelerate_web3_trans({
                'request_id': 'original-request-id',
                'gas_price': '50',
                'gas_limit': '30000'
            })
        """
        required_fields = ["request_id", "gas_price", "gas_limit"]
        for field in required_fields:
            if field not in params:
                raise ValueError(f"Required parameters: {', '.join(required_fields)}")

        response = self.post(
            "/api/mpc/web3/pending",
            {
                "request_id": params["request_id"],
                "gas_price": params["gas_price"],
                "gas_limit": params["gas_limit"],
            },
        )
        return self.validate_response(response)

    def get_web3_trans_records(self, request_ids: list) -> Dict[str, Any]:
        """
        Gets Web3 transaction records.

        Args:
            request_ids: Request IDs (list of strings, up to 100)

        Returns:
            Web3 transaction records

        Example:
            records = web3_api.get_web3_trans_records(['req-1', 'req-2'])
        """
        if not request_ids or not isinstance(request_ids, list) or len(request_ids) == 0:
            raise ValueError(
                'Parameter "request_ids" is required and must be a non-empty list'
            )

        response = self.get(
            "/api/mpc/web3/trans_list",
            {"ids": ",".join(request_ids)},
        )
        return self.validate_response(response)

    def sync_web3_trans_records(self, max_id: int = 0) -> Dict[str, Any]:
        """
        Synchronizes Web3 transaction records.

        Args:
            max_id: Starting ID of Web3 records (default: 0)

        Returns:
            Synchronized Web3 transaction records

        Example:
            records = web3_api.sync_web3_trans_records(0)
        """
        response = self.get(
            "/api/mpc/web3/sync_trans_list", {"max_id": max_id}
        )
        return self.validate_response(response)
