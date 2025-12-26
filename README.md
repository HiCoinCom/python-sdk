# ChainUp Custody Python SDK

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

ChainUp Custody 官方 Python SDK - 为数字资产托管提供完整的解决方案。

> 🔄 **基于 JavaScript SDK**: 本项目根据 [ChainUp Custody JavaScript SDK](https://github.com/HiCoinCom/js-sdk) 生成，确保跨语言 API 的一致性。

## ✨ 特性

- 🔐 **WaaS（钱包即服务）** - 完整的托管钱包 API 集成（6 个 API）
- 🔑 **MPC（多方计算）** - 安全的分布式密钥管理（9 个 API）
- 🔒 **交易签名** - MpcSignUtil 支持提现和 Web3 交易签名
- 🏗️ **现代架构** - 面向对象设计，使用 Builder 模式
- 📝 **完整的类型提示** - 符合 Python 类型注解标准
- ✅ **生产就绪** - 经过企业级环境验证
- 🚀 **易于集成** - 简单直观的 API
- 🔒 **与 Java/JS SDK 一致** - 请求/响应加密流程完全对齐

## 📦 安装

```bash
pip install chainup-custody-sdk
```

或从源码安装:

```bash
git clone https://github.com/ChainUp-Custody/python-sdk.git
cd python-sdk
pip install -e .
```

## 🚀 快速开始

### WaaS（托管）API

```python
from chainup_custody_sdk import WaasClient

# 使用 Builder 模式创建 WaaS 客户端
client = (
    WaasClient.new_builder()
    .set_host("https://api.custody.chainup.com")
    .set_app_id("your-app-id")
    .set_private_key("-----BEGIN PRIVATE KEY-----\n...")
    .set_public_key("-----BEGIN PUBLIC KEY-----\n...")
    .set_debug(True)
    .build()
)

# 用户操作
user_api = client.get_user_api()
user = user_api.register_email_user({"email": "user@example.com"})

# 账户操作
account_api = client.get_account_api()
balance = account_api.get_user_account({
    "uid": user["id"],
    "symbol": "BTC"
})

# 转账操作
transfer_api = client.get_transfer_api()
result = transfer_api.account_transfer({
    "request_id": "transfer_001",
    "symbol": "USDT",
    "amount": "100.5",
    "from": "user1",
    "to": "user2"
})
```

### MPC 钱包 API

```python
from chainup_custody_sdk import MpcClient

# 创建 MPC 客户端
mpc_client = (
    MpcClient.new_builder()
    .set_app_id("your-app-id")
    .set_rsa_private_key("-----BEGIN PRIVATE KEY-----\n...")
    .set_api_key("your-api-key")
    .set_domain("https://mpc-api.custody.chainup.com")
    .set_sign_private_key("-----BEGIN PRIVATE KEY-----\n...")  # 可选：用于提现/Web3交易签名
    .build()
)

# 创建钱包
wallet_api = mpc_client.get_wallet_api()
wallet = wallet_api.create_wallet({
    "sub_wallet_name": "My Wallet",
    "app_show_status": 1
})

# 提现
withdraw_api = mpc_client.get_withdraw_api()
result = withdraw_api.withdraw({
    "request_id": "unique-request-id",
    "sub_wallet_id": wallet["sub_wallet_id"],
    "symbol": "ETH",
    "amount": "0.1",
    "address_to": "0x123..."
})
```

### 使用自定义加密提供者

SDK 支持自定义加密实现（如 HSM、KMS 等）：

```python
from chainup_custody_sdk import WaasClient, ICryptoProvider

class MyCustomCryptoProvider(ICryptoProvider):
    def __init__(self, hsm_client):
        super().__init__()
        self.hsm_client = hsm_client

    def encrypt_with_private_key(self, data: str) -> str:
        # 使用 HSM/KMS 进行加密
        return self.hsm_client.encrypt(data)

    def decrypt_with_public_key(self, encrypted_data: str) -> str:
        # 使用 HSM/KMS 进行解密
        return self.hsm_client.decrypt(encrypted_data)

    def sign(self, data: str) -> str:
        return self.hsm_client.sign(data)

    def verify(self, data: str, signature: str) -> bool:
        return self.hsm_client.verify(data, signature)

# 使用自定义加密提供者
client = (
    WaasClient.new_builder()
    .set_host("https://api.custody.chainup.com")
    .set_app_id("your-app-id")
    .set_crypto_provider(MyCustomCryptoProvider(my_hsm_client))
    .build()
)
```

## 📚 API 参考

### WaaS 客户端 APIs

#### UserApi - 用户管理

- `register_mobile_user(params)` - 手机号注册用户
- `register_email_user(params)` - 邮箱注册用户
- `get_mobile_user(params)` - 获取用户信息（手机）
- `get_email_user(params)` - 获取用户信息（邮箱）
- `sync_user_list(params)` - 同步用户列表（分页）

#### AccountApi - 账户管理

- `get_user_account(params)` - 获取用户账户余额
- `get_user_address(params)` - 获取/创建充值地址
- `get_company_account(params)` - 获取公司账户信息
- `get_user_address_info(params)` - 通过地址获取用户信息
- `sync_user_address_list(params)` - 同步地址列表（分页）

#### BillingApi - 账单管理

- `withdraw(params)` - 创建提现请求
- `withdraw_list(params)` - 查询提现记录
- `sync_withdraw_list(params)` - 同步提现记录（分页）
- `deposit_list(params)` - 获取充值记录
- `sync_deposit_list(params)` - 同步充值记录（分页）
- `miner_fee_list(params)` - 查询矿工费记录
- `sync_miner_fee_list(params)` - 同步矿工费记录（分页）

#### CoinApi - 币种管理

- `get_coin_list(params)` - 获取支持的币种列表

#### TransferApi - 转账管理

- `account_transfer(params)` - 商户内部转账
- `get_account_transfer_list(params)` - 查询转账记录
- `sync_account_transfer_list(params)` - 同步转账记录（分页）

#### AsyncNotifyApi - 异步通知

- `notify_request(cipher)` - 解密充值/提现通知
- `verify_request(cipher)` - 解密提现二次验证请求
- `verify_response(withdraw)` - 加密二次验证响应

### MPC 客户端 APIs

#### WalletApi - 钱包管理

- `create_wallet(params)` - 创建钱包
- `create_wallet_address(params)` - 创建钱包地址
- `query_wallet_address(params)` - 查询钱包地址
- `get_wallet_assets(params)` - 获取钱包资产
- `change_wallet_show_status(params)` - 修改钱包显示状态
- `get_wallet_list(params)` - 获取钱包列表

#### DepositApi - 充值管理

- `get_deposit_records(params)` - 获取充值记录
- `sync_deposit_records(params)` - 同步充值记录（分页）

#### WithdrawApi - 提现管理

- `withdraw(params)` - 发起提现
- `get_withdraw_records(params)` - 获取提现记录
- `sync_withdraw_records(params)` - 同步提现记录（分页）

## 🔧 开发要求

- Python 3.7+
- requests >= 2.25.0
- pycryptodome >= 3.15.0

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

## 📞 支持

- 文档：[ChainUp Custody 官方文档](https://custodydocs-zh.chainup.com/)
- Issues：[GitHub Issues](https://github.com/ChainUp-Custody/python-sdk/issues)
- Email：support@chainup.com

## 🔗 相关链接

- [JavaScript SDK](https://github.com/HiCoinCom/js-sdk)
- [Java SDK](https://github.com/ChainUp-Custody/java-sdk)
- [官方网站](https://www.chainup.com/)
  python sdk for Chainup custody
