#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自定义加密提供者示例
"""
import sys
import os

# 添加项目根目录到 Python 路径（允许在不安装的情况下运行）
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from chainup_custody_sdk import WaasClient, ICryptoProvider


class MyCustomCryptoProvider(ICryptoProvider):
    """
    自定义加密提供者示例
    可以集成 HSM、KMS 或其他加密服务
    """

    def __init__(self, hsm_client):
        """
        初始化自定义加密提供者

        Args:
            hsm_client: HSM/KMS 客户端
        """
        super().__init__()
        self.hsm_client = hsm_client

    def encrypt_with_private_key(self, data: str) -> str:
        """
        使用私钥加密数据

        Args:
            data: 待加密的数据

        Returns:
            加密后的数据（URL-safe base64编码）
        """
        # 实现使用 HSM/KMS 的加密逻辑
        encrypted = self.hsm_client.encrypt(data)
        return encrypted

    def decrypt_with_public_key(self, encrypted_data: str) -> str:
        """
        使用公钥解密数据

        Args:
            encrypted_data: 加密的数据（URL-safe base64编码）

        Returns:
            解密后的数据
        """
        # 实现使用 HSM/KMS 的解密逻辑
        decrypted = self.hsm_client.decrypt(encrypted_data)
        return decrypted

    def sign(self, data: str) -> str:
        """
        签名数据

        Args:
            data: 待签名的数据

        Returns:
            签名（base64编码）
        """
        signature = self.hsm_client.sign(data)
        return signature

    def verify(self, data: str, signature: str) -> bool:
        """
        验证签名

        Args:
            data: 原始数据
            signature: 签名（base64编码）

        Returns:
            签名是否有效
        """
        return self.hsm_client.verify(data, signature)


def main():
    # 假设有一个 HSM 客户端
    class MockHSMClient:
        def encrypt(self, data):
            # 模拟加密
            return f"encrypted_{data}"

        def decrypt(self, encrypted_data):
            # 模拟解密
            return encrypted_data.replace("encrypted_", "")

        def sign(self, data):
            # 模拟签名
            return f"signature_of_{data}"

        def verify(self, data, signature):
            # 模拟验证
            expected = f"signature_of_{data}"
            return signature == expected

    hsm_client = MockHSMClient()
    custom_crypto = MyCustomCryptoProvider(hsm_client)

    # 创建 WaaS 客户端，使用自定义加密提供者
    client = (
        WaasClient.new_builder()
        .set_host("https://api.custody.chainup.com")
        .set_app_id("your-app-id")
        .set_crypto_provider(custom_crypto)
        .set_debug(True)
        .build()
    )

    # 使用客户端
    user_api = client.get_user_api()
    print("Client created with custom crypto provider")

    # 测试加密和解密
    test_data = "Hello, World!"
    encrypted = custom_crypto.encrypt_with_private_key(test_data)
    print(f"Encrypted: {encrypted}")

    decrypted = custom_crypto.decrypt_with_public_key(encrypted)
    print(f"Decrypted: {decrypted}")

    # 测试签名和验证
    signature = custom_crypto.sign(test_data)
    print(f"Signature: {signature}")

    is_valid = custom_crypto.verify(test_data, signature)
    print(f"Signature valid: {is_valid}")


if __name__ == "__main__":
    main()
