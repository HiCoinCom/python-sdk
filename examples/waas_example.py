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
        .set_app_id("")
        .set_private_key("")
        .set_public_key("" )
        .set_debug(False)
        .build()
    )
    uid = 15036904  # 替换为实际用户ID

    # ============== 用户管理 ==============
    user_api = client.get_user_api()

    # 注册用户（邮箱）
    try:
        user = user_api.register_email_user({"email": "user12@example.com"})
        print(f"Created user: {user}")
    except Exception as e:
        print(f"Error creating user: {e}")

    # 获取用户信息
    user_info = user_api.get_email_user({"email": "user12@example.com"})
    print(f"User info: {user_info}")

    # 同步用户列表
    users = user_api.sync_user_list(0)
    print(f"User list: {len(users)} users synced ")
    
    # 注册手机用户
    try:
        user_mobile = user_api.register_mobile_user(
            {"country": "86", "mobile": "13800000011"}
        )
        print(f"Created mobile user: {user_mobile}")
    except Exception as e:
        print(f"Error creating mobile user: {e}")
    
    # 获取手机用户信息
    user_info_mobile = user_api.get_mobile_user({"country": "86", "mobile": "13800000011"})
    print(f"Mobile User info: {user_info_mobile}")  

    
    # ============== 账户管理 ==============
    account_api = client.get_account_api()

    # 获取用户账户余额
    account = account_api.get_user_account({"uid": uid, "symbol": "APTOS"})
    print(f"Account balance: {account}")

    # 获取充值地址
    address = account_api.get_user_address({"uid": uid, "symbol": "APTOS"})
    print(f"Deposit address: {address}")
    
    # aqcuire user address info
    address_info = account_api.get_user_address_info({"address": address["address"]})
    print(f"Address info: {address_info}")
    
    # 获取公司账户信息 
    company_account = account_api.get_company_account({"symbol": "APTOS"})
    print(f"Company account: {company_account}")

      # 同步用户地址列表  
    address_list = account_api.sync_user_address_list(0)
    print(f"User address list: {len(address_list)} addresses synced ")  
    
    # ============== 币种管理 ==============
    coin_api = client.get_coin_api()

    # 获取支持的币种列表
    coins = coin_api.get_coin_list()
    print(f"Supported coins: {len(coins)} coins")

    # ============== 账单管理 ==============
    billing_api = client.get_billing_api()

    # 提现
    try:
        withdraw_result = billing_api.withdraw(
            {
                "request_id": "withdraw_001",
                "from_uid": uid,
                "to_address": "0x0f1dc222af5ea2660ff84ae91adc48f1cb2d4991f1e6569dd24d94599c335a06",
                "amount": "0.001",
                "symbol": "APTOS",
            }
        )
        print(f"Withdraw result: {withdraw_result}")
    except Exception as e:
        print(f"Error during withdrawal: {e}")

    # 查询提现记录
    withdrawals = billing_api.withdraw_list(["withdraw_001"])
    print(f"Withdrawals: {len(withdrawals)} records found")
    
    # 同步提现记录
    synced_withdrawals = billing_api.sync_withdraw_list(0)
    print(f"Synced Withdrawals: {len(synced_withdrawals)} records found")

    # 查询充值记录
    deposits = billing_api.deposit_list(["123", "456"])
    print(f"Deposits: {len(deposits)} records found") 

    # 同步充值记录
    deposits = billing_api.sync_deposit_list(0)
    print(f"Deposits: {len(deposits)} records synced ")
    
    # 查询miner fee记录
    miner_fees = billing_api.miner_fee_list(["12"])
    print(f"Miner Fees: {len(miner_fees)} records found")
    
    # 同步miner fee记录
    synced_miner_fees = billing_api.sync_miner_fee_list(0)
    print(f"Synced Miner Fees: {len(synced_miner_fees)} records found ")

    # ============== 转账管理 ==============
    transfer_api = client.get_transfer_api()

    # 商户内部转账
    try:
        transfer_result = transfer_api.account_transfer(
            {
                "request_id": "transfer_001",
                "symbol": "USDT",
                "amount": "100.5",
                "from": str(uid),
                "to": "1123",  # 替换为实际目标用户ID
                "remark": "Internal transfer",
            }
        )
        print(f"Transfer result: {transfer_result}")
    except Exception as e:
        print(f"Error during transfer: {e}")

    # 查询转账记录
    transfers = transfer_api.get_account_transfer_list(
        {"ids": "transfer_001", "ids_type": "request_id"}
    )
    print(f"Transfers: {len(transfers)} records found")
    
    # 同步转账记录
    synced_transfers = transfer_api.sync_account_transfer_list(0)
    print(f"Synced Transfers: {len(synced_transfers)} records found ")  
    
    # ============== 异步通知 ==============
    async_notify_api = client.get_async_notify_api()

    # 解密通知数据（假设收到加密的通知）
    encrypted_notification = "jhoA9MtGotqWxqEtB27SwCtJCo9JSIxh2B6m8CItrPQj2gsm6rw-ti1qY5tNP52qXg60FLK49cFj-a84m-57z8aT-Vo-YyJPTcM8Qpuyjj5Pf8tAcbBjBHganULYNPjCCkzgH5n5dlMZIp0tmpc7nV7Pp6hi63KjGGNTfAAbWp7QOVukAsQeQyBFPeKhlVEhq8xqQEN2yg_T1jHRUjIdlTDn2LG_i2tI0MlDpPg5FHL6cViSVM23WBPhJnAFOOrGhaqq06YtVG2m8_x_pLTyI5ZK61Bv0HnDUuIkDuRqNXyhko0sG9uGuKWJ3maWfUc9bSb0VcWPHeWnYUrcE2M9TVtwTEKdcImqZnvjc12YUh_Oz2a9VNls_XN_gTRbeIiTUGsiXX1Yq6OkCCxrsCgD0AXz0KOX4uphZldXq17ZO7sU21-b1y0rsk0qY6PbKRYpp4hhdeKpEfB2gckhf1rc9h17j0ufri4LqsE4EccGuQD4JcSrT5RLY4QRil4wdIO9ZPmhb-Od3zqT9OYPSvPg0QVCVpw-Tn17WfsZw2xB9gO8uzvGcvz9TfUrI8zKg6b6roTR9xt0m0oqMCyhrjAlU35QUh54MHAWI22A3WJkR4d4KhTOrq-2KuCg7Obi3SCoZmVWb28tztUwN6ttc4PJmM370g_YNCiv5Q6F95QgozYAGpu7Kc8ckcsORixNAUpqTCYaZHmST7bxCXDGPaL45H4zHe6IkU-Tf06rY7DoKeMgjGTz3Pb8hrXRXdSCYz9y0MjwGledXqnLiww0Dn_q-qWgOqQs6NeiLG5IqWKJG2e0buav2l_fH-biflRHjpidaTvFnTMUPf9k9-ygWwiWDzM9OD0X-mNdEI6WNe_27O9CtmUTxlBgRJ2tYyhF32a3flQXaA4m34PPXD_HyxFYRQXfqTt_7uaV7NinsnwN8Ll9ccFdXw8BuANu8j24zvBP0zvUyo9d1ywqn0Cw2wt-vPUWF7sZifTLkdr9O7mcAN08ByaIc1MR5ULI-lUsfi6U"  # 从回调接收的加密数据
    notification_data = async_notify_api.notify_request(encrypted_notification)
    if notification_data:
        print(f"Notification: {notification_data}")
        
    # 解密提现二次验证请求数据
    encrypted_verify_request = "jhoA9MtGotqWxqEtB27SwCtJCo9JSIxh2B6m8CItrPQj2gsm6rw-ti1qY5tNP52qXg60FLK49cFj-a84m-57z8aT-Vo-YyJPTcM8Qpuyjj5Pf8tAcbBjBHganULYNPjCCkzgH5n5dlMZIp0tmpc7nV7Pp6hi63KjGGNTfAAbWp7QOVukAsQeQyBFPeKhlVEhq8xqQEN2yg_T1jHRUjIdlTDn2LG_i2tI0MlDpPg5FHL6cViSVM23WBPhJnAFOOrGhaqq06YtVG2m8_x_pLTyI5ZK61Bv0HnDUuIkDuRqNXyhko0sG9uGuKWJ3maWfUc9bSb0VcWPHeWnYUrcE2M9TVtwTEKdcImqZnvjc12YUh_Oz2a9VNls_XN_gTRbeIiTUGsiXX1Yq6OkCCxrsCgD0AXz0KOX4uphZldXq17ZO7sU21-b1y0rsk0qY6PbKRYpp4hhdeKpEfB2gckhf1rc9h17j0ufri4LqsE4EccGuQD4JcSrT5RLY4QRil4wdIO9ZPmhb-Od3zqT9OYPSvPg0QVCVpw-Tn17WfsZw2xB9gO8uzvGcvz9TfUrI8zKg6b6roTR9xt0m0oqMCyhrjAlU35QUh54MHAWI22A3WJkR4d4KhTOrq-2KuCg7Obi3SCoZmVWb28tztUwN6ttc4PJmM370g_YNCiv5Q6F95QgozYAGpu7Kc8ckcsORixNAUpqTCYaZHmST7bxCXDGPaL45H4zHe6IkU-Tf06rY7DoKeMgjGTz3Pb8hrXRXdSCYz9y0MjwGledXqnLiww0Dn_q-qWgOqQs6NeiLG5IqWKJG2e0buav2l_fH-biflRHjpidaTvFnTMUPf9k9-ygWwiWDzM9OD0X-mNdEI6WNe_27O9CtmUTxlBgRJ2tYyhF32a3flQXaA4m34PPXD_HyxFYRQXfqTt_7uaV7NinsnwN8Ll9ccFdXw8BuANu8j24zvBP0zvUyo9d1ywqn0Cw2wt-vPUWF7sZifTLkdr9O7mcAN08ByaIc1MR5ULI-lUsfi6U"
    verify_request_data = async_notify_api.verify_request(encrypted_verify_request)
    if verify_request_data:
        print(f"Verify Request: {verify_request_data}") 
        
    # verify_response 示例略，类似于 notify_request 和 verify_request
    # 解密提现二次验证响应数据
    verify_response_data = async_notify_api.verify_response(verify_request_data)
    if verify_response_data:
        print(f"Verify Response: {verify_response_data}") 


if __name__ == "__main__":
    main()
