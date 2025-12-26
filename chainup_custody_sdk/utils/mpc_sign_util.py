"""
MPC Signature Utility
Provides signature generation for MPC withdrawal and Web3 transactions
"""
import hashlib
import re
from typing import Dict, Any, Optional
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64


class MpcSignUtil:
    """
    MPC Signature Utility Class.
    
    Provides signature generation for MPC operations:
    - Withdrawal transaction signing
    - Web3 transaction signing
    
    Signing process:
    1. Sort parameters by key (ASCII order)
    2. Format as k1=v1&k2=v2 (lowercase)
    3. Generate MD5 hash of the formatted string
    4. Sign the MD5 hash with RSA-SHA256 private key
    5. Return Base64 encoded signature
    """

    @staticmethod
    def generate_withdraw_sign(withdraw_params: Dict[str, Any], sign_private_key: str) -> str:
        """
        Generates signature for MPC withdrawal.

        Args:
            withdraw_params: Withdrawal parameters
                - request_id: Request ID
                - sub_wallet_id: Sub-wallet ID
                - symbol: Coin symbol
                - address_to: Destination address
                - amount: Withdrawal amount
                - memo: Address memo (optional)
                - outputs: UTXO outputs (optional)
            sign_private_key: RSA private key for signing (PEM format)

        Returns:
            Base64 encoded signature

        Example:
            signature = MpcSignUtil.generate_withdraw_sign({
                'request_id': 'unique-id',
                'sub_wallet_id': 123,
                'symbol': 'ETH',
                'address_to': '0x123...',
                'amount': '0.1'
            }, private_key)
        """
        if not withdraw_params or not sign_private_key:
            return ""

        sign_params_map = {
            "request_id": withdraw_params.get("request_id"),
            "sub_wallet_id": withdraw_params.get("sub_wallet_id"),
            "symbol": withdraw_params.get("symbol"),
            "address_to": withdraw_params.get("address_to"),
            "amount": withdraw_params.get("amount"),
            "memo": withdraw_params.get("memo"),
            "outputs": withdraw_params.get("outputs"),
        }

        sign_data = MpcSignUtil.params_sort(sign_params_map)
        if not sign_data:
            return ""

        return MpcSignUtil.sign(sign_data, sign_private_key)

    @staticmethod
    def generate_web3_sign(web3_params: Dict[str, Any], sign_private_key: str) -> str:
        """
        Generates signature for Web3 transaction.

        Args:
            web3_params: Web3 transaction parameters
                - request_id: Request ID
                - sub_wallet_id: Sub-wallet ID
                - main_chain_symbol: Main chain symbol
                - interactive_contract: Interactive contract address
                - amount: Transaction amount
                - input_data: Input data
            sign_private_key: RSA private key for signing (PEM format)

        Returns:
            Base64 encoded signature

        Example:
            signature = MpcSignUtil.generate_web3_sign({
                'request_id': 'unique-id',
                'sub_wallet_id': 123,
                'main_chain_symbol': 'ETH',
                'interactive_contract': '0x123...',
                'amount': '0',
                'input_data': '0x...'
            }, private_key)
        """
        if not web3_params or not sign_private_key:
            return ""

        sign_params_map = {
            "request_id": web3_params.get("request_id"),
            "sub_wallet_id": web3_params.get("sub_wallet_id"),
            "main_chain_symbol": web3_params.get("main_chain_symbol"),
            "interactive_contract": web3_params.get("interactive_contract"),
            "amount": web3_params.get("amount"),
            "input_data": web3_params.get("input_data"),
        }

        sign_data = MpcSignUtil.params_sort(sign_params_map)
        if not sign_data:
            return ""

        return MpcSignUtil.sign(sign_data, sign_private_key)

    @staticmethod
    def params_sort(params: Dict[str, Any]) -> str:
        """
        Sorts parameters and formats them for signing.
        
        Rules:
        - Parameters are formatted as k1=v1&k2=v2
        - Keys are sorted in ASCII ascending order
        - Empty values are excluded from signature
        - Numeric values must not end with 0 (e.g., 1.0001000 becomes 1.0001)
        - Result is converted to lowercase

        Args:
            params: Parameters to sort

        Returns:
            Sorted and formatted parameter string

        Example:
            >>> MpcSignUtil.params_sort({'amount': '1.0001000', 'symbol': 'ETH'})
            'amount=1.0001&symbol=eth'
        """
        if not params:
            return ""

        sorted_params = {}

        # Process each parameter
        for key, value in params.items():
            # Skip empty values
            if value is None or value == "":
                continue

            # Convert to string
            value = str(value)

            # Remove trailing zeros from numeric amounts
            if key == "amount" and value:
                # Use regex to remove trailing zeros after decimal point
                # 1.0001000 -> 1.0001, 1.0 -> 1
                value = re.sub(r"(\.\d*?)0+$", r"\1", value)
                value = re.sub(r"\.$", "", value)

            sorted_params[key] = value

        # Sort keys in ASCII order
        sorted_keys = sorted(sorted_params.keys())

        # Build the parameter string
        parts = []
        for key in sorted_keys:
            parts.append(f"{key}={sorted_params[key]}")

        # Join with & and convert to lowercase
        return "&".join(parts).lower()

    @staticmethod
    def sign(sign_data: str, sign_private_key: str) -> str:
        """
        Signs data using RSA private key with SHA256.
        
        Process:
        1. Convert sorted params to lowercase
        2. Generate MD5 hash of the params string
        3. Sign the MD5 hash with RSA-SHA256
        4. Return Base64 encoded signature

        Args:
            sign_data: Data to sign (sorted parameters string)
            sign_private_key: RSA private key (PEM format or Base64 encoded)

        Returns:
            Base64 encoded signature

        Example:
            >>> signature = MpcSignUtil.sign('amount=1.0&symbol=eth', private_key)
        """
        if not sign_data or not sign_private_key:
            return ""

        try:
            # Step 1: Generate MD5 hash of the data
            md5_hash = hashlib.md5(sign_data.encode("utf-8")).hexdigest()

            # Step 2: Load RSA private key
            # Support both PEM format and raw Base64 encoded keys
            key = None
            private_key_str = sign_private_key.strip()
            
            # Check if it's already in PEM format
            if private_key_str.startswith("-----BEGIN"):
                try:
                    key = RSA.import_key(private_key_str)
                except Exception:
                    pass
            
            # Try as raw Base64 (PKCS#8 DER format)
            if key is None:
                try:
                    # Remove any whitespace/newlines
                    clean_key = private_key_str.replace("\n", "").replace("\r", "").replace(" ", "")
                    der_data = base64.b64decode(clean_key)
                    key = RSA.import_key(der_data)
                except Exception:
                    pass
            
            # Try wrapping as PKCS#8 PEM
            if key is None:
                try:
                    clean_key = private_key_str.replace("\n", "").replace("\r", "").replace(" ", "")
                    pem_key = f"-----BEGIN PRIVATE KEY-----\n{clean_key}\n-----END PRIVATE KEY-----"
                    key = RSA.import_key(pem_key)
                except Exception:
                    pass
            
            # Try wrapping as PKCS#1 PEM
            if key is None:
                try:
                    clean_key = private_key_str.replace("\n", "").replace("\r", "").replace(" ", "")
                    pem_key = f"-----BEGIN RSA PRIVATE KEY-----\n{clean_key}\n-----END RSA PRIVATE KEY-----"
                    key = RSA.import_key(pem_key)
                except Exception as e:
                    raise ValueError(f"Failed to import RSA private key in any format: {str(e)}")
            
            if key is None:
                raise ValueError("Failed to import RSA private key: unsupported format")

            # Step 3: Sign the MD5 hash with RSA-SHA256
            h = SHA256.new(md5_hash.encode("utf-8"))
            signature = pkcs1_15.new(key).sign(h)

            # Step 4: Return Base64 encoded signature
            return base64.b64encode(signature).decode("utf-8")

        except Exception as e:
            print(f"MPC sign error: {str(e)}")
            return ""

    @staticmethod
    def md5(data: str) -> str:
        """
        Calculates MD5 hash of a string.

        Args:
            data: Data to hash

        Returns:
            MD5 hash in hexadecimal

        Example:
            >>> MpcSignUtil.md5('test')
            '098f6bcd4621d373cade4e832627b4f6'
        """
        return hashlib.md5(data.encode("utf-8")).hexdigest()
