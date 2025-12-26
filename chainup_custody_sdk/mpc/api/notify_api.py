"""
Notify API - MPC notification handling operations
"""
from typing import Optional
from chainup_custody_sdk.mpc.api.mpc_base_api import MpcBaseApi
import json


class NotifyApi(MpcBaseApi):
    """
    Notify API - MPC notification handling operations.
    Provides methods for decrypting MPC async notifications (webhooks).
    """

    def __init__(self, config):
        """
        Creates a new NotifyApi instance.

        Args:
            config: MpcConfig object
        """
        super().__init__(config)

    def notify_request(self, cipher: str) -> Optional[dict]:
        """
        Decrypts deposit and withdrawal notification parameters.
        Used to decrypt encrypted notification data received from MPC callbacks.

        Args:
            cipher: Encrypted notification data

        Returns:
            Decrypted notification arguments, or None if decryption fails

        Example:
            notify_data = notify_api.notify_request(encrypted_data)
            if notify_data:
                print('Notify type:', notify_data['side'])  # 'deposit' or 'withdraw'
                print('Sub wallet ID:', notify_data['sub_wallet_id'])
                print('Symbol:', notify_data['symbol'])
                print('Amount:', notify_data['amount'])
        """
        if not cipher:
            if self.config.debug:
                print("[MpcNotify] Cipher cannot be empty")
            return None

        try:
            # Decrypt the cipher text using crypto provider
            raw = self.crypto_provider.decrypt_with_public_key(cipher)

            if self.config.debug:
                print(f"[MpcNotify] Decrypted data: {raw}")

            if not raw:
                print("[MpcNotify] Decrypt cipher returned None")
                return None

            # Parse JSON to notification arguments
            notify = json.loads(raw)
            if not notify:
                print("[MpcNotify] JSON decode returned None")
                return None

            return notify

        except json.JSONDecodeError as e:
            print(f"[MpcNotify] JSON decode error: {str(e)}")
            return None
        except Exception as e:
            print(f"[MpcNotify] Failed to decrypt notification: {str(e)}")
            return None
