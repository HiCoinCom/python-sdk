"""
Crypto Provider - Interface and implementations for encryption/decryption
"""
from abc import ABC, abstractmethod
import base64
import hashlib
from typing import Optional
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


class ICryptoProvider(ABC):
    """
    Interface for crypto provider implementations.
    Allows custom encryption/decryption implementations (e.g., HSM, KMS).
    """

    @abstractmethod
    def encrypt_with_private_key(self, data: str) -> str:
        """
        Encrypts data using the private key.

        Args:
            data: Data to encrypt

        Returns:
            Encrypted data (URL-safe base64 encoded)
        """
        pass

    @abstractmethod
    def decrypt_with_public_key(self, encrypted_data: str) -> str:
        """
        Decrypts data using the public key.

        Args:
            encrypted_data: Encrypted data (URL-safe base64 encoded)

        Returns:
            Decrypted data
        """
        pass

    def sign(self, data: str) -> str:
        """
        Signs data (optional, for transaction signing).

        Args:
            data: Data to sign

        Returns:
            Signature (base64 encoded)
        """
        raise NotImplementedError("Sign method not implemented")

    def verify(self, data: str, signature: str) -> bool:
        """
        Verifies signature (optional).

        Args:
            data: Original data
            signature: Signature to verify

        Returns:
            True if signature is valid
        """
        raise NotImplementedError("Verify method not implemented")


class RsaCryptoProvider(ICryptoProvider):
    """
    Default RSA Crypto Provider.
    Implements ICryptoProvider using RSA encryption with segment encryption/decryption
    for long data (matches Java SDK RSAHelper).
    """

    # RSA key size is 2048 bits = 256 bytes
    # Max encrypt block = 256 - 11 (PKCS1 padding) = 245 bytes, but Java uses 234
    MAX_ENCRYPT_BLOCK = 234
    # Max decrypt block = 256 bytes
    MAX_DECRYPT_BLOCK = 256

    def __init__(
        self,
        private_key: Optional[str] = None,
        public_key: Optional[str] = None,
        charset: str = "UTF-8",
        sign_private_key: Optional[str] = None,
    ):
        """
        Creates a new RSA crypto provider instance.

        Args:
            private_key: RSA private key in PEM format
            public_key: RSA public key in PEM format
            charset: Character encoding (default: UTF-8)
            sign_private_key: RSA private key for signing in PEM format (optional, uses private_key if not set)
        """
        self.private_key = self._format_rsa_key(private_key, "private") if private_key else None
        self.public_key = self._format_rsa_key(public_key, "public") if public_key else None
        self.charset = charset
        self.sign_private_key = self._format_rsa_key(sign_private_key, "private") if sign_private_key else None

    @staticmethod
    def _format_rsa_key(key: str, key_type: str) -> str:
        """
        Formats RSA key to proper PEM format.

        Args:
            key: RSA key string
            key_type: 'private' or 'public'

        Returns:
            Properly formatted PEM key
        """
        key = key.strip()
        
        # Remove existing headers/footers if present
        key = key.replace("-----BEGIN PRIVATE KEY-----", "")
        key = key.replace("-----END PRIVATE KEY-----", "")
        key = key.replace("-----BEGIN RSA PRIVATE KEY-----", "")
        key = key.replace("-----END RSA PRIVATE KEY-----", "")
        key = key.replace("-----BEGIN PUBLIC KEY-----", "")
        key = key.replace("-----END PUBLIC KEY-----", "")
        key = key.replace("-----BEGIN RSA PUBLIC KEY-----", "")
        key = key.replace("-----END RSA PUBLIC KEY-----", "")
        key = key.replace("\n", "").replace("\r", "").replace(" ", "")

        # Add proper headers/footers
        if key_type == "private":
            return f"-----BEGIN PRIVATE KEY-----\n{key}\n-----END PRIVATE KEY-----"
        else:
            return f"-----BEGIN PUBLIC KEY-----\n{key}\n-----END PUBLIC KEY-----"

    def encrypt_with_private_key(self, data: str) -> str:
        """
        Encrypts data using the private key with segment encryption.
        Matches Java SDK RSAHelper.encryptByPrivateKey() with segment encryption.
        
        Note: This is a non-standard RSA usage where we encrypt with private key
        so that the receiver can decrypt with our public key.

        Args:
            data: Data to encrypt

        Returns:
            URL-safe base64 encoded encrypted data
        """
        if not self.private_key:
            raise ValueError("Private key is not set")

        try:
            data_bytes = data.encode("utf-8")
            key = RSA.import_key(self.private_key)
            key_size = key.size_in_bytes()
            
            # For RSA with PKCS#1 v1.5 padding, max data size is key_size - 11
            max_block = key_size - 11

            # Segment encryption: encrypt in blocks
            encrypted_chunks = []
            offset = 0
            input_len = len(data_bytes)

            while offset < input_len:
                block_size = min(max_block, input_len - offset)
                chunk = data_bytes[offset : offset + block_size]

                # Add PKCS#1 v1.5 padding manually
                # Format: 0x00 0x01 [0xFF padding] 0x00 [data]
                padding_len = key_size - len(chunk) - 3
                padded = b'\x00\x01' + (b'\xff' * padding_len) + b'\x00' + chunk
                
                # Raw RSA operation with private key: m^d mod n
                padded_int = int.from_bytes(padded, byteorder='big')
                encrypted_int = pow(padded_int, key.d, key.n)
                encrypted_bytes = encrypted_int.to_bytes(key_size, byteorder='big')

                encrypted_chunks.append(encrypted_bytes)
                offset += block_size

            # Combine all encrypted chunks
            combined = b"".join(encrypted_chunks)

            # Convert to URL-safe base64
            return base64.urlsafe_b64encode(combined).decode("utf-8").rstrip("=")

        except Exception as e:
            raise RuntimeError(f"Failed to encrypt with private key: {str(e)}")

    def decrypt_with_public_key(self, encrypted_data: str) -> str:
        """
        Decrypts data using the public key with segment decryption.
        Matches Java SDK RSAHelper.decryptByPublicKey() with segment decryption.
        
        Note: This is a non-standard RSA usage where the server encrypts with 
        its private key and the client decrypts with the server's public key.
        This is essentially a "raw RSA" operation (signature verification flow).

        Args:
            encrypted_data: URL-safe base64 encrypted data to decrypt

        Returns:
            Decrypted data
        """
        if not self.public_key:
            raise ValueError("Public key is not set")

        try:
            # Convert URL-safe base64 back to standard base64
            padding = len(encrypted_data) % 4
            if padding:
                encrypted_data += "=" * (4 - padding)

            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data)
            key = RSA.import_key(self.public_key)
            
            # Get key size in bytes
            key_size = key.size_in_bytes()

            # Segment decryption: decrypt in blocks of key_size
            decrypted_chunks = []
            offset = 0
            input_len = len(encrypted_bytes)

            while offset < input_len:
                block_size = min(key_size, input_len - offset)
                chunk = encrypted_bytes[offset : offset + block_size]

                # Use raw RSA operation to decrypt with public key
                # This is equivalent to signature verification without the hash check
                # encrypted = m^d mod n (server encrypts with private key)
                # decrypted = encrypted^e mod n (client decrypts with public key)
                encrypted_int = int.from_bytes(chunk, byteorder='big')
                decrypted_int = pow(encrypted_int, key.e, key.n)
                
                # Convert back to bytes
                decrypted_bytes = decrypted_int.to_bytes(key_size, byteorder='big')
                
                # Remove PKCS#1 v1.5 padding: 0x00 0x01 [padding 0xFF...] 0x00 [data]
                # or for encryption: 0x00 0x02 [random padding] 0x00 [data]
                if len(decrypted_bytes) >= 11:
                    # Find the 0x00 separator after padding
                    separator_idx = -1
                    if decrypted_bytes[0:2] == b'\x00\x01' or decrypted_bytes[0:2] == b'\x00\x02':
                        for i in range(2, len(decrypted_bytes)):
                            if decrypted_bytes[i] == 0:
                                separator_idx = i
                                break
                    
                    if separator_idx > 0:
                        decrypted_chunks.append(decrypted_bytes[separator_idx + 1:])
                    else:
                        # No valid padding found, might be raw data
                        decrypted_chunks.append(decrypted_bytes.lstrip(b'\x00'))
                else:
                    decrypted_chunks.append(decrypted_bytes.lstrip(b'\x00'))
                
                offset += block_size

            # Combine all decrypted chunks
            combined = b"".join(decrypted_chunks)
            return combined.decode("utf-8")

        except Exception as e:
            raise RuntimeError(f"Failed to decrypt with public key: {str(e)}")

    def sign(self, data: str) -> str:
        """
        Signs data using sign_private_key if set, otherwise uses private_key.
        
        Process (matches MpcSignUtil.sign):
        1. Generate MD5 hash of the data
        2. Sign the MD5 hash with RSA-SHA256
        3. Return Base64 encoded signature

        Args:
            data: Data to sign

        Returns:
            Base64 encoded signature
        """
        # Use sign_private_key if set, otherwise fall back to private_key
        signing_key = self.sign_private_key if self.sign_private_key else self.private_key
        
        if not signing_key:
            raise ValueError("Neither sign_private_key nor private_key is set")

        try:
            # Step 1: Generate MD5 hash of the data
            md5_hash = hashlib.md5(data.encode("utf-8")).hexdigest()
            
            # Step 2: Sign the MD5 hash with RSA-SHA256
            key = RSA.import_key(signing_key)
            hash_obj = SHA256.new(md5_hash.encode("utf-8"))
            signature = pkcs1_15.new(key).sign(hash_obj)
            
            # Step 3: Return Base64 encoded signature
            return base64.b64encode(signature).decode("utf-8")
        except Exception as e:
            raise RuntimeError(f"Failed to sign data: {str(e)}")

    def verify(self, data: str, signature: str) -> bool:
        """
        Verifies signature using public key.

        Args:
            data: Original data
            signature: Base64 encoded signature

        Returns:
            True if signature is valid
        """
        if not self.public_key:
            raise ValueError("Public key is not set")

        try:
            key = RSA.import_key(self.public_key)
            hash_obj = SHA256.new(data.encode("utf-8"))
            signature_bytes = base64.b64decode(signature)
            pkcs1_15.new(key).verify(hash_obj, signature_bytes)
            return True
        except (ValueError, TypeError):
            return False
