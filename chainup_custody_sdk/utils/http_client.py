"""
HTTP Client - Handles HTTP communication with APIs
"""
import json
from typing import Dict, Any, Optional
import requests


class BaseHttpClient:
    """
    Base HTTP Client Class.
    Provides common HTTP request functionality for both WaaS and MPC APIs.
    """

    def __init__(self, config, content_type="application/x-www-form-urlencoded"):
        """
        Creates a new HTTP client instance.

        Args:
            config: Config object (WaasConfig or MpcConfig)
            content_type: Content-Type header value
        """
        self.config = config
        self.session = requests.Session()
        if content_type:
            self.session.headers.update({"Content-Type": content_type})

    def request(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        Executes an HTTP request.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API path
            data: Request data
            headers: Additional headers

        Returns:
            Response body as string

        Raises:
            RuntimeError: If request fails
        """
        data = data or {}
        headers = headers or {}

        url = self.config.get_url(path)

        request_headers = {**self.session.headers, **headers}

        if self.config.debug:
            print(f"[HTTP Request]: {method} {url}")
            print(f"[HTTP Data]: {data}")

        try:
            if method == "POST":
                response = self.session.post(
                    url, data=data, headers=request_headers, timeout=30
                )
            elif method == "GET":
                response = self.session.get(
                    url, params=data, headers=request_headers, timeout=30
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            if response.status_code != 200:
                raise RuntimeError(
                    f"HTTP {response.status_code}: {response.text}"
                )

            if self.config.debug:
                print(f"[HTTP Response]: {response.text}")

            return response.text

        except requests.RequestException as e:
            raise RuntimeError(f"HTTP request failed: {str(e)}")

    def post(self, path: str, data: Optional[Dict[str, Any]] = None) -> str:
        """
        Executes a POST request.

        Args:
            path: API path
            data: Request data

        Returns:
            Response body as string
        """
        return self.request("POST", path, data)

    def get(self, path: str, data: Optional[Dict[str, Any]] = None) -> str:
        """
        Executes a GET request.

        Args:
            path: API path
            data: Request data

        Returns:
            Response body as string
        """
        return self.request("GET", path, data)


class HttpClient(BaseHttpClient):
    """
    WaaS HTTP Client Class (backward compatible).
    Handles HTTP communication with the WaaS API.
    """

    def __init__(self, config):
        """
        Creates a new WaaS HTTP client instance.

        Args:
            config: WaasConfig object
        """
        super().__init__(config, "application/x-www-form-urlencoded")
