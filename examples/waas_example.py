#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WaaS API 使用示例
"""
import sys
import os

# 添加项目根目录到 Python 路径（允许在不安装的情况下运行）
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 检查依赖
try:
    from chainup_custody_sdk import WaasClient
except ImportError as e:
    print("=" * 60)
    print("❌ 缺少必要的依赖")
    print("=" * 60)
    print(f"\n错误: {e}\n")
    print("请先安装依赖:")
    print("  pip3 install pycryptodome requests")
    print("\n或者:")
    print("  pip3 install -r requirements.txt")
    print("=" * 60)
    sys.exit(1)


def main():
    # 创建 WaaS 客户端
    client = (
        WaasClient.new_builder()
        .set_host("https://api.custody.chainup.com")
        .set_app_id("your-app-id")
        .set_private_key(
            """-----BEGIN PRIVATE KEY-----
your-private-key-content
-----END PRIVATE KEY-----"""
        )
        .set_public_key(
            """-----BEGIN PUBLIC KEY-----
chainup-public-key-content
-----END PUBLIC KEY-----"""
        )
        .set_debug(False)
        .build()
    )

    # ============== 用户管理 ==============
    user_api = client.get_user_api()

    # 注册用户（邮箱）
    user = user_api.register_email_user({"email": "user@example.com"})
    print(f"Created user: {user}")

    # 获取用户信息
    user_info = user_api.get_email_user({"email": "user@example.com"})
    print(f"User info: {user_info}")

    # 同步用户列表
    users = user_api.sync_user_list({"max_id": 0})
    print(f"User list: {users}")

    # ============== 账户管理 ==============
    account_api = client.get_account_api()

    # 获取用户账户余额
    account = account_api.get_user_account({"uid": user["uid"], "symbol": "BTC"})
    print(f"Account balance: {account}")

    # 获取充值地址
    address = account_api.get_user_address({"uid": user["uid"], "symbol": "ETH"})
    print(f"Deposit address: {address}")

    # ============== 币种管理 ==============
    coin_api = client.get_coin_api()

    # 获取支持的币种列表
    coins = coin_api.get_coin_list()
    print(f"Supported coins: {coins}")

    # ============== 账单管理 ==============
    billing_api = client.get_billing_api()

    # 提现
    withdraw_result = billing_api.withdraw(
        {
            "request_id": "withdraw_001",
            "from_uid": user["uid"],
            "to_address": "0x1234567890abcdef1234567890abcdef12345678",
            "amount": "1.5",
            "symbol": "ETH",
        }
    )
    print(f"Withdraw result: {withdraw_result}")

    # 查询提现记录
    withdrawals = billing_api.withdraw_list({"ids": "withdraw_001"})
    print(f"Withdrawals: {withdrawals}")

    # 同步充值记录
    deposits = billing_api.sync_deposit_list({"max_id": 0})
    print(f"Deposits: {deposits}")

    # ============== 转账管理 ==============
    transfer_api = client.get_transfer_api()

    # 商户内部转账
    transfer_result = transfer_api.account_transfer(
        {
            "request_id": "transfer_001",
            "symbol": "USDT",
            "amount": "100.5",
            "from": "user1",
            "to": "user2",
            "remark": "Internal transfer",
        }
    )
    print(f"Transfer result: {transfer_result}")

    # 查询转账记录
    transfers = transfer_api.get_account_transfer_list(
        {"ids": "transfer_001", "ids_type": "request_id"}
    )
    print(f"Transfers: {transfers}")

    # ============== 异步通知 ==============
    async_notify_api = client.get_async_notify_api()

    # 解密通知数据（假设收到加密的通知）
    encrypted_notification = "..."  # 从回调接收的加密数据
    notification_data = async_notify_api.notify_request(encrypted_notification)
    if notification_data:
        print(f"Notification: {notification_data}")


if __name__ == "__main__":
    main()
