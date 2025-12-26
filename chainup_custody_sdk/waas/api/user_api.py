"""
User API - User management and registration operations
"""
from typing import Dict, Any, List, Optional
from chainup_custody_sdk.waas.api.base_api import BaseApi


class UserApi(BaseApi):
    """
    User API - User management and registration operations.
    Provides methods for user registration, information retrieval, and coin list queries.
    """

    def __init__(self, config):
        """
        Creates a new UserApi instance.

        Args:
            config: WaasConfig object
        """
        super().__init__(config)

    def register_mobile_user(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Registers a new user using mobile phone.

        Args:
            params: Registration parameters
                - country: Country code (e.g., '86')
                - mobile: Mobile phone number

        Returns:
            User registration result containing uid

        Example:
            result = user_api.register_mobile_user({
                'country': '86',
                'mobile': '13800000000'
            })
        """
        response = self.post("/user/createUser", params)
        return self.validate_response(response)

    def register_email_user(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Registers a new user using email.

        Args:
            params: Registration parameters
                - email: Email address

        Returns:
            User registration result containing uid

        Example:
            result = user_api.register_email_user({
                'email': 'user@example.com'
            })
        """
        response = self.post("/user/registerEmail", params)
        return self.validate_response(response)

    def get_mobile_user(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gets user information by mobile phone.

        Args:
            params: Query parameters
                - country: Country code (e.g., '86')
                - mobile: Mobile phone number

        Returns:
            User information

        Example:
            user_info = user_api.get_mobile_user({
                'country': '86',
                'mobile': '13800000000'
            })
        """
        response = self.post("/user/info", params)
        return self.validate_response(response)

    def get_email_user(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gets user information by email.

        Args:
            params: Query parameters
                - email: User email

        Returns:
            User information

        Example:
            user_info = user_api.get_email_user({
                'email': 'user@example.com'
            })
        """
        response = self.post("/user/info", params)
        return self.validate_response(response)

    def sync_user_list(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Syncs user list by max ID (pagination).

        Args:
            params: Query parameters
                - max_id: Maximum user ID for pagination (0 for first sync)

        Returns:
            Synced user list

        Example:
            users = user_api.sync_user_list({'max_id': 0})
        """
        response = self.post("/user/syncList", params)
        return self.validate_response(response)
