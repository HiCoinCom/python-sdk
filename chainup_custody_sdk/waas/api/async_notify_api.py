"""
Async Notify API - Asynchronous notification management
"""
from typing import Dict, Any, Optional
import json
from chainup_custody_sdk.waas.api.base_api import BaseApi


class AsyncNotifyApi(BaseApi):
    """
    Async Notify API - Asynchronous notification management.
    Provides methods for decrypting and managing webhook notifications.
    """

    def __init__(self, config):
        """
        Creates a new AsyncNotifyApi instance.

        Args:
            config: WaasConfig object
        """
        super().__init__(config)

    def notify_request(self, cipher: str) -> Optional[Dict[str, Any]]:
        """
        Decrypts deposit and withdrawal notification parameters.
        Used to decrypt encrypted notification data received from WaaS callbacks.

        Args:
            cipher: Encrypted notification data

        Returns:
            Decrypted notification arguments, or None if decryption fails

        Example:
            notify_data = async_notify_api.notify_request(encrypted_data)
            if notify_data:
                print('Notify type:', notify_data.get('side'))  # 'deposit' or 'withdraw'
        """
        if not cipher:
            if self.config.debug:
                print("[AsyncNotify] Cipher cannot be empty")
            return None

        try:
            # Decrypt the cipher text using public key
            raw = self.crypto_provider.decrypt_with_public_key(cipher)

            if self.config.debug:
                print(f"[AsyncNotify] Decrypted data: {raw}")

            if not raw:
                print("[AsyncNotify] Decrypt cipher returned null")
                return None

            # Parse JSON to notification arguments
            notify = json.loads(raw)
            if not notify:
                print("[AsyncNotify] JSON decode returned null")
                return None

            return notify
        except Exception as error:
            print(f"[AsyncNotify] Failed to decrypt notification: {str(error)}")
            return None

    def verify_request(self, cipher: str) -> Optional[Dict[str, Any]]:
        """
        Decrypts withdrawal secondary verification request parameters.
        Used to decrypt verification request data for withdrawal operations
        that require additional confirmation.

        Args:
            cipher: Encrypted verification request data

        Returns:
            Decrypted withdrawal arguments, or None if decryption fails

        Example:
            withdraw_data = async_notify_api.verify_request(encrypted_data)
            if withdraw_data:
                print('Withdraw request:', withdraw_data.get('request_id'))
        """
        if not cipher:
            if self.config.debug:
                print("[AsyncNotify] VerifyRequest cipher cannot be empty")
            return None

        try:
            # Decrypt the cipher text
            raw = self.crypto_provider.decrypt_with_public_key(cipher)

            if self.config.debug:
                print(f"[AsyncNotify] VerifyRequest decrypted data: {raw}")

            if not raw:
                print("[AsyncNotify] VerifyRequest decrypt returned null")
                return None

            # Parse JSON to withdrawal arguments
            withdraw = json.loads(raw)
            if not withdraw:
                print("[AsyncNotify] VerifyRequest JSON decode returned null")
                return None

            return withdraw
        except Exception as error:
            print(f"[AsyncNotify] Failed to decrypt verify request: {str(error)}")
            return None

    def verify_response(self, withdraw: Dict[str, Any]) -> Optional[str]:
        """
        Encrypts the secondary verification withdrawal response data.
        Used to encrypt the response data when confirming or rejecting
        a withdrawal that requires secondary verification.

        Args:
            withdraw: Withdrawal arguments to encrypt

        Returns:
            Encrypted response data, or None if encryption fails

        Example:
            response_data = async_notify_api.verify_response({
                'request_id': 'xxx',
                'status': 1  # 1=approve, 2=reject
            })
        """
        if not withdraw:
            print("[AsyncNotify] VerifyResponse withdraw cannot be empty")
            return None

        try:
            # Convert to JSON string
            withdraw_json = json.dumps(withdraw, separators=(",", ":"))

            # Encrypt with private key
            raw = self.crypto_provider.encrypt_with_private_key(withdraw_json)

            if not raw:
                print("[AsyncNotify] VerifyResponse encrypt returned null")
                return None

            return raw
        except Exception as error:
            print(f"[AsyncNotify] Failed to encrypt verify response: {str(error)}")
            return None
