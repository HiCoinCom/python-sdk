"""
MPC Base API - Base class for all MPC API implementations
"""
import json
import time
from typing import Dict, Any, Optional
from chainup_custody_sdk.utils.mpc_http_client import MpcHttpClient
from chainup_custody_sdk.utils.crypto_provider import RsaCryptoProvider


class MpcBaseApi:
    """
    MPC Base API Class.
    Provides common functionality for all MPC API implementations.
    Implements the same encryption flow as Java SDK:
    - Request: encrypt params with private key, send as {app_id, data}
    - Response: decrypt data field with public key
    """

    def __init__(self, config):
        """
        Creates a base MPC API instance.

        Args:
            config: MpcConfig object
        """
        self.config = config
        self.http_client = MpcHttpClient(config)

        # Use custom crypto provider or create default RSA provider
        if config.crypto_provider:
            self.crypto_provider = config.crypto_provider
        elif config.rsa_private_key:
            self.crypto_provider = RsaCryptoProvider(
                private_key=config.rsa_private_key,
                public_key=config.waas_public_key or "",  # WaaS server public key
                charset="UTF-8",
            )
        else:
            self.crypto_provider = None

    def _build_request_args(self, data: Optional[Dict[str, Any]] = None) -> str:
        """
        Builds the request args JSON with common parameters.
        Matches Java SDK: args.setCharset(), args.setTime(), args.toJson()

        Args:
            data: API-specific request data

        Returns:
            JSON string of request args
        """
        data = data or {}
        args = {**data, "time": int(time.time() * 1000), "charset": "utf-8"}
        return json.dumps(args)

    def _execute_request(
        self, method: str, path: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Executes an MPC API request.
        Flow matches Java SDK invoke():
        1. Serialize params to JSON
        2. Encrypt with private key
        3. Send only app_id and encrypted data
        4. Decrypt response data with public key

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API path
            data: Request data

        Returns:
            API response (decrypted if encrypted)
        """
        # Step 1: Build request args JSON (matches Java SDK args.toJson())
        raw_json = self._build_request_args(data)

        if self.config.debug:
            print(f"[MPC Request Args]: {raw_json}")

        # Step 2: Encrypt with private key (matches Java SDK dataCrypto.encode(raw))
        encrypted_data = ""
        if self.crypto_provider:
            try:
                encrypted_data = self.crypto_provider.encrypt_with_private_key(raw_json)
                if self.config.debug:
                    print(f"[MPC Encrypted Data]: {encrypted_data[:100]}...")
            except Exception as e:
                raise RuntimeError(f"Failed to encrypt request data: {str(e)}")

        # Step 3: Send request with only app_id and data
        response = self.http_client.request(method, path, encrypted_data)

        if self.config.debug:
            print(f"[MPC Response]: {response}")

        # Step 4: Check if response has encrypted data field and decrypt
        if response and "data" in response and isinstance(response["data"], str):
            # MPC API returns encrypted data, need to decrypt with public key
            if self.crypto_provider:
                try:
                    decrypted = self.crypto_provider.decrypt_with_public_key(
                        response["data"]
                    )
                    if self.config.debug:
                        print(f"[MPC Decrypted]: {decrypted}")
                    # Parse decrypted JSON and return complete response
                    decrypted_data = json.loads(decrypted)
                    return decrypted_data
                except Exception as e:
                    if self.config.debug:
                        print(f"[MPC Decrypt Error]: {str(e)}")
                    # If decryption fails, might be an error response, return as-is
                    return response

        return response

    def post(self, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executes a POST request.

        Args:
            path: API path
            data: Request data

        Returns:
            API response
        """
        return self._execute_request("POST", path, data)

    def get(self, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executes a GET request.

        Args:
            path: API path
            data: Request data

        Returns:
            API response
        """
        return self._execute_request("GET", path, data)

    def validate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates response and handles errors.
        Matches WaaS SDK validateResponse behavior:
        - Check if code is 0 (success)
        - Raise exception for error responses
        - Return data field for successful responses

        Args:
            response: API response

        Returns:
            The 'data' field from successful response, or empty dict if no data

        Raises:
            RuntimeError: If response code indicates an error
        """
        if isinstance(response, str):
            try:
                response = json.loads(response)
            except json.JSONDecodeError as e:
                raise RuntimeError(f"Invalid JSON response: {response}")

        code = response.get("code")
        
        # Check if code is 0 (success) - can be int or string
        if code != 0 and code != "0":
            msg = response.get("msg", "Unknown error")
            raise RuntimeError(f"API Error [{code}]: {msg}")

        # Return data field, or empty dict if not present
        return response.get("data", {}) if response.get("data") != "" else {}
