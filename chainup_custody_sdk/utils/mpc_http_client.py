"""
MPC HTTP Client - Handles HTTP communication with the MPC API
"""
import json
from typing import Dict, Any, Optional
import requests
from chainup_custody_sdk.utils.http_client import BaseHttpClient


class MpcHttpClient(BaseHttpClient):
    """
    MPC HTTP Client Class.
    Handles HTTP communication with the MPC API.
    Implements the same request format as Java SDK:
    - Request params: app_id + data (encrypted with private key)
    - Response data: encrypted with private key, decrypt with public key
    """

    def __init__(self, config):
        """
        Creates a new MPC HTTP client instance.

        Args:
            config: MpcConfig object
        """
        super().__init__(config, None)  # MPC doesn't set Content-Type in headers

    def request(
        self,
        method: str,
        path: str,
        encrypted_data: str,
    ) -> Dict[str, Any]:
        """
        Executes an HTTP request.
        Request format matches Java SDK: only app_id and data (encrypted) are sent.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API path
            encrypted_data: RSA encrypted request data

        Returns:
            Response data as dict

        Raises:
            RuntimeError: If request fails
        """
        url = self.config.get_url(path)

        # Only two parameters: app_id and data (encrypted)
        # This matches Java SDK: Args params = new Args(this.cfg.getAppId(), data);
        params = {"app_id": self.config.app_id, "data": encrypted_data}

        if self.config.debug:
            print(f"[MPC HTTP Request]: {method} {url}")
            print(
                f"[MPC HTTP Params]: app_id={params['app_id']}, data={encrypted_data[:100] if encrypted_data else ''}..."
            )

        try:
            if method == "POST":
                # Use form submission (application/x-www-form-urlencoded)
                response = self.session.post(url, data=params, timeout=30)
            elif method == "GET":
                response = self.session.get(url, params=params, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            if response.status_code != 200:
                raise RuntimeError(
                    f"MPC HTTP {response.status_code}: {response.text}"
                )

            if self.config.debug:
                print(f"[MPC HTTP Response]: {response.text}")

            # Parse JSON response
            return response.json()

        except requests.RequestException as e:
            raise RuntimeError(f"MPC HTTP request failed: {str(e)}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse MPC response: {str(e)}")

    def post(self, path: str, encrypted_data: str) -> Dict[str, Any]:
        """
        Executes a POST request.

        Args:
            path: API path
            encrypted_data: Encrypted request data

        Returns:
            Response data as dict
        """
        return self.request("POST", path, encrypted_data)

    def get(self, path: str, encrypted_data: str) -> Dict[str, Any]:
        """
        Executes a GET request.

        Args:
            path: API path
            encrypted_data: Encrypted request data

        Returns:
            Response data as dict
        """
        return self.request("GET", path, encrypted_data)
