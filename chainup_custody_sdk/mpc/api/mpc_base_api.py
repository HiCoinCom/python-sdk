"""
MPC Base API - Base class for all MPC API implementations
"""
from __future__ import annotations

import json
import time
from typing import Dict, Any, Optional, Union

from chainup_custody_sdk.utils.mpc_http_client import MpcHttpClient
from chainup_custody_sdk.utils.crypto_provider import RsaCryptoProvider
from chainup_custody_sdk.exceptions import ApiError, CryptoError, NetworkError
from chainup_custody_sdk.logger import LoggerMixin


class MpcBaseApi(LoggerMixin):
    """
    MPC Base API Class.
    
    Provides common functionality for all MPC API implementations.
    Implements the same encryption flow as Java SDK:
    - Request: encrypt params with private key, send as {app_id, data}
    - Response: decrypt data field with public key
    """
    
    __slots__ = ("config", "http_client", "crypto_provider")

    def __init__(self, config) -> None:
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
                sign_private_key=config.sign_private_key,
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
        
        Raises:
            CryptoError: If encryption/decryption fails
            NetworkError: If HTTP request fails
            ApiError: If API returns an error
        """
        # Step 1: Build request args JSON (matches Java SDK args.toJson())
        raw_json = self._build_request_args(data)

        self._logger.debug(f"Request args: {raw_json}")

        # Step 2: Encrypt with private key (matches Java SDK dataCrypto.encode(raw))
        encrypted_data = ""
        if self.crypto_provider:
            try:
                encrypted_data = self.crypto_provider.encrypt_with_private_key(raw_json)
                self._logger.debug(f"Encrypted data: {encrypted_data[:100]}...")
            except Exception as e:
                raise CryptoError(f"Failed to encrypt request data: {str(e)}")

        # Step 3: Send request with only app_id and data
        try:
            response = self.http_client.request(method, path, encrypted_data)
        except RuntimeError as e:
            raise NetworkError(str(e))

        self._logger.debug(f"Response: {response}")

        # Step 4: Check if response has encrypted data field and decrypt
        if response and "data" in response and isinstance(response["data"], str):
            # MPC API returns encrypted data, need to decrypt with public key
            if self.crypto_provider:
                try:
                    decrypted = self.crypto_provider.decrypt_with_public_key(
                        response["data"]
                    )
                    self._logger.debug(f"Decrypted: {decrypted}")
                    # Parse decrypted JSON and return complete response
                    decrypted_data = json.loads(decrypted)
                    return decrypted_data
                except Exception as e:
                    self._logger.warning(f"Decrypt error: {str(e)}")
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

    def validate_response(self, response: Union[Dict[str, Any], str]) -> Any:
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
            ApiError: If response code indicates an error
        """
        if isinstance(response, str):
            try:
                response = json.loads(response)
            except json.JSONDecodeError as e:
                raise ApiError(f"Invalid JSON response: {response}")

        code = response.get("code")
        
        # Check if code is 0 (success) - can be int or string
        if code != 0 and code != "0":
            msg = response.get("msg", "Unknown error")
            raise ApiError(message=msg, code=int(code) if code else None)

        # Return data field, or empty dict if not present
        return response.get("data", {}) if response.get("data") != "" else {}
