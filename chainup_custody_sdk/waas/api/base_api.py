"""
Base API Class - Provides common functionality for all WaaS API implementations
"""
import json
import time
from typing import Dict, Any, Optional
from chainup_custody_sdk.utils.http_client import HttpClient
from chainup_custody_sdk.utils.crypto_provider import RsaCryptoProvider


class BaseApi:
    """
    Base API Class.
    Provides common functionality for all WaaS API implementations.
    Implements the same encryption flow as Java SDK:
    - Request: encrypt params with private key, send as {app_id, data}
    - Response: decrypt data field with public key
    """

    def __init__(self, config):
        """
        Creates a base API instance.

        Args:
            config: WaasConfig object
        """
        self.config = config
        self.http_client = HttpClient(config)

        # Use custom crypto provider or create default RSA provider
        if config.crypto_provider:
            self.crypto_provider = config.crypto_provider
        else:
            self.crypto_provider = RsaCryptoProvider(
                private_key=config.private_key,
                public_key=config.public_key,
                charset=config.charset,
            )

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
        args = {
            **data,
            "time": int(time.time() * 1000),  # Milliseconds timestamp
            "charset": self.config.charset or "utf-8",
        }
        return json.dumps(args, separators=(",", ":"))

    def _execute_request(
        self, method: str, path: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Executes an API request with signing and encryption.
        Flow matches Java SDK WaasApi.invoke():
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
            RuntimeError: If request or encryption fails
        """
        # Step 1: Build request args JSON (matches Java SDK args.toJson())
        raw_json = self._build_request_args(data)

        if self.config.debug:
            print(f"[WaaS Request Args]: {raw_json}")

        # Step 2: Encrypt with private key (matches Java SDK dataCrypto.encode(raw))
        encrypted_data = ""
        if self.crypto_provider:
            try:
                encrypted_data = self.crypto_provider.encrypt_with_private_key(raw_json)
                if self.config.debug:
                    print(f"[WaaS Encrypted Data]: {encrypted_data[:100]}...")
            except Exception as e:
                raise RuntimeError(f"Failed to encrypt request data: {str(e)}")

        # Step 3: Send request with only app_id and data
        request_data = {"app_id": self.config.app_id, "data": encrypted_data}

        response_text = self.http_client.request(method, path, request_data)

        if self.config.debug:
            print(f"[WaaS Response]: {response_text}")

        # Step 4: Parse response and decrypt data if needed
        try:
            parsed_response = json.loads(response_text)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON response: {response_text}")

        # Check if response has encrypted data field and decrypt
        if (
            parsed_response
            and "data" in parsed_response
            and isinstance(parsed_response["data"], str)
        ):
            if self.crypto_provider:
                try:
                    decrypted = self.crypto_provider.decrypt_with_public_key(
                        parsed_response["data"]
                    )
                    if self.config.debug:
                        print(f"[WaaS Decrypted]: {decrypted}")
                    # Parse decrypted JSON and return complete response
                    decrypted_data = json.loads(decrypted)
                    return decrypted_data
                except Exception as e:
                    if self.config.debug:
                        print(f"[WaaS Decrypt Error]: {str(e)}")
                    # If decryption fails, might be an error response, return as-is
                    return parsed_response

        return parsed_response

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

    def validate_response(self, response: Any) -> Any:
        """
        Validates response and handles errors.

        Args:
            response: API response

        Returns:
            Validated response data

        Raises:
            RuntimeError: If response indicates an error
        """
        if isinstance(response, str):
            try:
                response = json.loads(response)
            except json.JSONDecodeError as e:
                raise RuntimeError(f"Invalid JSON response: {response}")

        if not isinstance(response, dict):
            return response

        code = response.get("code")
        if code is not None and str(code) != "0":
            msg = response.get("msg", "Unknown error")
            raise RuntimeError(f"API Error [{code}]: {msg}")

        return response.get("data", response)
