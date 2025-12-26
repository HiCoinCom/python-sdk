# 快速开始指南

本指南将帮助您快速上手 ChainUp Custody Python SDK。

## 安装

```bash
pip install chainup-custody-sdk
```

或从源码安装：

```bash
git clone https://github.com/ChainUp-Custody/python-sdk.git
cd python-sdk
pip install -e .
```

## 基本配置

### 获取 API 凭证

在开始之前，您需要从 ChainUp Custody 平台获取以下凭证：

1. **App ID** - 您的应用程序 ID
2. **Private Key** - 您的 RSA 私钥（用于签名请求）
3. **Public Key** - ChainUp 的公钥（用于验证响应）

## WaaS API 快速示例

### 1. 创建客户端

```python
from chainup_custody_sdk import WaasClient

client = (
    WaasClient.new_builder()
    .set_app_id("your-app-id")
    .set_private_key("""-----BEGIN PRIVATE KEY-----
your-private-key-content
-----END PRIVATE KEY-----""")
    .set_public_key("""-----BEGIN PUBLIC KEY-----
chainup-public-key-content
-----END PUBLIC KEY-----""")
    .set_debug(True)  # 开发环境建议开启
    .build()
)
```

### 2. 用户管理

```python
# 获取 UserApi 实例
user_api = client.get_user_api()

# 注册用户（邮箱）
user = user_api.register_email_user({
    "email": "user@example.com"
})
print(f"User ID: {user['uid']}")

# 获取用户信息
user_info = user_api.get_email_user({
    "email": "user@example.com"
})
```

### 3. 账户管理

```python
# 获取 AccountApi 实例
account_api = client.get_account_api()

# 获取用户账户余额
account = account_api.get_user_account({
    "uid": user['uid'],
    "symbol": "BTC"
})
print(f"Balance: {account['balance']}")

# 获取充值地址
address = account_api.get_user_address({
    "uid": user['uid'],
    "symbol": "ETH"
})
print(f"Deposit address: {address['address']}")
```

### 4. 提现操作

```python
# 获取 BillingApi 实例
billing_api = client.get_billing_api()

# 创建提现请求
result = billing_api.withdraw({
    "request_id": "withdraw_001",  # 唯一请求ID
    "from_uid": user['uid'],
    "to_address": "0x1234567890...",
    "amount": "1.5",
    "symbol": "ETH"
})
print(f"Withdraw ID: {result['withdraw_id']}")
```

## MPC API 快速示例

### 1. 创建客户端

```python
from chainup_custody_sdk import MpcClient

mpc_client = (
    MpcClient.new_builder()
    .set_app_id("your-app-id")
    .set_rsa_private_key("""-----BEGIN PRIVATE KEY-----
your-rsa-private-key-content
-----END PRIVATE KEY-----""")
    .set_api_key("your-api-key")
    .set_debug(True)
    .build()
)
```

### 2. 钱包管理

```python
# 获取 WalletApi 实例
wallet_api = mpc_client.get_wallet_api()

# 创建钱包
wallet = wallet_api.create_wallet({
    "sub_wallet_name": "My Wallet",
    "app_show_status": 1  # 1=显示, 2=隐藏
})
print(f"Wallet ID: {wallet['sub_wallet_id']}")

# 创建钱包地址
address = wallet_api.create_wallet_address({
    "sub_wallet_id": wallet['sub_wallet_id'],
    "symbol": "ETH"
})
print(f"Address: {address['address']}")
```

### 3. 提现操作

```python
# 获取 WithdrawApi 实例
withdraw_api = mpc_client.get_withdraw_api()

# 发起提现
result = withdraw_api.withdraw({
    "request_id": "unique-id-001",
    "sub_wallet_id": wallet['sub_wallet_id'],
    "symbol": "ETH",
    "amount": "0.1",
    "address_to": "0x1234567890..."
})
print(f"Withdraw ID: {result['withdraw_id']}")
```

### 4. 查询充值记录

```python
# 获取 DepositApi 实例
deposit_api = mpc_client.get_deposit_api()

# 同步充值记录
deposits = deposit_api.sync_deposit_records({
    "max_id": 0  # 从头开始
})
for deposit in deposits['data']:
    print(f"Deposit: {deposit['amount']} {deposit['symbol']}")
```

## 错误处理

```python
try:
    user = user_api.register_email_user({
        "email": "user@example.com"
    })
except ValueError as e:
    print(f"Validation error: {e}")
except RuntimeError as e:
    print(f"Request error: {e}")
```

## 调试模式

在开发环境中，建议开启调试模式：

```python
client = (
    WaasClient.new_builder()
    # ... 其他配置 ...
    .set_debug(True)  # 打印请求/响应详情
    .build()
)
```

## 下一步

- 查看 [examples/](../examples/) 目录获取更多示例
- 阅读 [README.md](../README.md) 了解完整 API 列表
- 访问 [官方文档](https://custodydocs-zh.chainup.com/) 获取详细的 API 说明

## 常见问题

### 如何处理异步通知？

```python
async_notify_api = client.get_async_notify_api()

# 从 webhook 接收到的加密数据
encrypted_data = request.POST.get('data')

# 解密通知
notification = async_notify_api.notify_request(encrypted_data)
if notification:
    print(f"Notification type: {notification['side']}")
    print(f"Amount: {notification['amount']}")
```

### 如何使用自定义加密提供者？

参见 [examples/custom_crypto_example.py](../examples/custom_crypto_example.py)

### 支持哪些 Python 版本？

Python 3.7 及以上版本
