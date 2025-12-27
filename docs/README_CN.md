# ChainUp Custody Python SDK

[![Python 版本](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![版本](https://img.shields.io/badge/version-1.1.0-orange.svg)](https://github.com/ChainUp-Custody/python-sdk)

ChainUp Custody 的 WaaS（钱包即服务）和 MPC（多方计算）API 的综合 Python SDK。

**[English Documentation](../README.md)**

## 特性

- 🔐 **WaaS API** - 钱包即服务，用于管理用户、账户、充值和提现
- 🔑 **MPC API** - 多方计算，实现安全的钱包管理
- 📝 **类型提示** - 完整的类型注解，提供更好的 IDE 支持
- 🛡️ **自定义异常** - 详细的错误处理，具有特定的异常类型
- 📊 **数据模型** - 基于 dataclass 的模型，实现类型安全的数据处理
- 🔧 **Builder 模式** - 流畅的 API，轻松配置客户端
- 🪵 **日志系统** - 可配置的日志系统
- ✅ **测试覆盖** - 全面的单元测试覆盖

## 安装

### 从源码安装

```bash
git clone https://github.com/ChainUp-Custody/python-sdk.git
cd python-sdk
pip install -e .
```

### 从 GitHub 安装

```bash
pip install git+https://github.com/HiCoinCom/python-sdk.git@main
```

### 开发环境安装

```bash
pip install -e ".[dev]"
```

## 快速开始

### WaaS 客户端

```python
from chainup_custody_sdk import WaasClient, ApiError

# 使用 Builder 模式创建客户端
client = (
    WaasClient.builder()
    .set_app_id("your-app-id")
    .set_private_key("your-rsa-private-key")
    .set_public_key("chainup-public-key")
    .set_debug(False)
    .build()
)

# 使用上下文管理器自动清理资源
with client:
    # 注册用户
    try:
        user = client.get_user_api().register_email_user({
            "email": "user@example.com"
        })
        print(f"用户已创建: {user}")
    except ApiError as e:
        print(f"API 错误: {e}")

    # 获取账户余额
    balance = client.get_account_api().get_user_account({
        "uid": 12345,
        "symbol": "ETH"
    })
    print(f"余额: {balance}")
```

### MPC 客户端

```python
from chainup_custody_sdk import MpcClient, ApiError

# 创建 MPC 客户端
client = (
    MpcClient.builder()
    .set_app_id("your-app-id")
    .set_rsa_private_key("your-rsa-private-key")
    .set_sign_private_key("your-sign-private-key")
    .set_waas_public_key("waas-public-key")
    .set_debug(False)
    .build()
)

with client:
    # 创建钱包
    try:
        wallet = client.get_wallet_api().create_wallet({
            "sub_wallet_name": "我的钱包",
            "app_show_status": 1
        })
        print(f"钱包已创建: {wallet}")
    except ApiError as e:
        print(f"错误: {e}")

    # 查询充值记录
    deposits = client.get_deposit_api().sync_deposit_records(0)
    print(f"充值记录: {deposits}")
```

## API 参考

### WaaS APIs

| API              | 描述               |
| ---------------- | ------------------ |
| `UserApi`        | 用户注册和管理     |
| `AccountApi`     | 账户余额和地址管理 |
| `BillingApi`     | 充值、提现和矿工费 |
| `CoinApi`        | 加密货币列表查询   |
| `TransferApi`    | 用户间内部转账     |
| `AsyncNotifyApi` | 回调通知处理       |

### MPC APIs

| API               | 描述             |
| ----------------- | ---------------- |
| `WalletApi`       | 钱包创建和管理   |
| `DepositApi`      | 充值记录查询     |
| `WithdrawApi`     | 提现操作         |
| `WorkspaceApi`    | 工作空间和链管理 |
| `AutoSweepApi`    | 自动归集配置     |
| `Web3Api`         | Web3 合约交互    |
| `TronResourceApi` | TRON 资源管理    |
| `NotifyApi`       | MPC 回调处理     |

## 错误处理

SDK 提供了自定义异常层次结构：

```python
from chainup_custody_sdk import (
    ChainUpError,      # 基础异常
    ApiError,          # API 请求错误
    ConfigError,       # 配置错误
    CryptoError,       # 加密/解密错误
    NetworkError,      # 网络连接错误
    ValidationError,   # 输入验证错误
    SignatureError,    # 签名验证错误
    RateLimitError,    # 限流错误
)

try:
    result = client.get_billing_api().withdraw({...})
except ApiError as e:
    print(f"API 错误 [{e.code}]: {e.message}")
except ConfigError as e:
    print(f"配置错误: {e}")
except ChainUpError as e:
    print(f"SDK 错误: {e}")
```

## API 错误码

| 错误码  | 常量                      | 描述                   |
| ------- | ------------------------- | ---------------------- |
| 0       | `SUCCESS`                 | 成功                   |
| 100001  | `SYSTEM_ERROR`            | 系统错误               |
| 100004  | `PARAM_INVALID`           | 请求参数不合法         |
| 100005  | `SIGN_ERROR`              | 签名校验失败           |
| 100007  | `IP_FORBIDDEN`            | 非法 IP                |
| 100015  | `MERCHANT_ID_INVALID`     | 商户 ID 无效           |
| 100016  | `MERCHANT_EXPIRED`        | 商户信息过期           |
| 110004  | `USER_FROZEN`             | 用户被冻结不可提现     |
| 110023  | `MOBILE_REGISTERED`       | 手机号已注册           |
| 110037  | `WITHDRAW_ADDRESS_RISK`   | 提现地址存在风险       |
| 110055  | `WITHDRAW_ADDRESS_ERROR`  | 提现地址错误           |
| 110065  | `USER_NOT_EXIST`          | 用户不存在             |
| 110078  | `AMOUNT_BELOW_MIN`        | 金额小于最小转出金额   |
| 110087  | `AMOUNT_EXCEED_MAX`       | 金额大于最大转出金额   |
| 110088  | `DUPLICATE_REQUEST`       | 请勿重复提交请求       |
| 110089  | `MOBILE_INVALID`          | 注册手机号不正确       |
| 110101  | `REGISTER_FAILED`         | 用户注册失败           |
| 110161  | `PRECISION_EXCEEDED`      | 超过提现最大支持精度   |
| 120202  | `COIN_NOT_SUPPORTED`      | 币种不支持             |
| 120206  | `CONFIRM_FAILED`          | 提现二次确认失败       |
| 120402  | `BALANCE_INSUFFICIENT`    | 余额不足               |
| 120403  | `FEE_INSUFFICIENT`        | 手续费余额不足         |
| 120404  | `AMOUNT_LESS_THAN_FEE`    | 金额小于等于手续费     |
| 900006  | `USER_RISK_FORBIDDEN`     | 用户存在风险，禁止提现 |
| 3040006 | `SELF_TRANSFER_FORBIDDEN` | 不能给自己转账         |

## 日志配置

配置日志用于调试：

```python
from chainup_custody_sdk import configure_logging, enable_debug_logging

# 启用调试日志
enable_debug_logging()

# 或使用自定义设置配置
configure_logging(level="DEBUG", format="%(asctime)s - %(name)s - %(message)s")
```

## 数据模型

SDK 提供基于 dataclass 的模型：

```python
from chainup_custody_sdk import (
    ApiResponse,
    WalletInfo,
    AddressInfo,
    TransactionRecord,
    CoinInfo,
    UserInfo,
    NotifyData,
    AssetBalance,
)

# 解析 API 响应
response = ApiResponse.from_dict(api_data)
if response.is_success:
    wallet = WalletInfo.from_dict(response.data)
    print(f"钱包 ID: {wallet.sub_wallet_id}")
```

## WaaS API 详细说明

### UserApi - 用户管理

```python
user_api = client.get_user_api()

# 手机号注册用户
user = user_api.register_mobile_user({
    "country": "86",        # 国家代码
    "mobile": "13800000000" # 手机号
})

# 邮箱注册用户
user = user_api.register_email_user({
    "email": "user@example.com"
})

# 获取用户信息
user_info = user_api.get_mobile_user({
    "country": "86",
    "mobile": "13800000000"
})

# 同步用户列表
users = user_api.sync_user_list(max_id=0)
```

### AccountApi - 账户管理

```python
account_api = client.get_account_api()

# 获取用户账户余额
account = account_api.get_user_account({
    "uid": 12345,
    "symbol": "BTC"
})

# 获取充值地址
address = account_api.get_user_address({
    "uid": 12345,
    "symbol": "ETH"
})

# 获取公司账户余额
company = account_api.get_company_account({
    "symbol": "ETH"
})

# 同步用户地址列表
addresses = account_api.sync_user_address_list(max_id=0)
```

### BillingApi - 账单管理

```python
billing_api = client.get_billing_api()

# 发起提现
result = billing_api.withdraw({
    "request_id": "unique-request-id",
    "from_uid": 12345,
    "to_address": "0x1234...",
    "amount": "1.5",
    "symbol": "ETH",
    "memo": "",              # 可选，地址备注
    "remark": "提现备注"      # 可选
})

# 查询提现记录
withdrawals = billing_api.withdraw_list(["request_id_1", "request_id_2"])

# 同步提现记录
synced = billing_api.sync_withdraw_list(max_id=0)

# 查询充值记录
deposits = billing_api.deposit_list(["123", "456"])

# 同步充值记录
synced = billing_api.sync_deposit_list(max_id=0)

# 查询矿工费记录
fees = billing_api.miner_fee_list(["fee_id_1"])

# 同步矿工费记录
synced = billing_api.sync_miner_fee_list(max_id=0)
```

### TransferApi - 转账管理

```python
transfer_api = client.get_transfer_api()

# 内部转账
result = transfer_api.account_transfer({
    "request_id": "transfer-001",
    "symbol": "USDT",
    "amount": "100.5",
    "from": "12345",      # 源用户ID
    "to": "67890",        # 目标用户ID
    "remark": "转账备注"
})

# 查询转账记录
transfers = transfer_api.get_account_transfer_list({
    "ids": "transfer-001",
    "ids_type": "request_id"  # 或 "receipt"
})

# 同步转账记录
synced = transfer_api.sync_account_transfer_list(max_id=0)
```

## MPC API 详细说明

### WalletApi - 钱包管理

```python
wallet_api = client.get_wallet_api()

# 创建钱包
wallet = wallet_api.create_wallet({
    "sub_wallet_name": "我的钱包",
    "app_show_status": 1  # 1=显示, 2=隐藏
})

# 创建钱包地址
address = wallet_api.create_wallet_address({
    "sub_wallet_id": 123,
    "symbol": "ETH"
})

# 查询钱包地址
addresses = wallet_api.query_wallet_address({
    "sub_wallet_id": 123,
    "symbol": "ETH",
    "max_id": 0
})

# 获取钱包余额
balance = wallet_api.get_wallet_balance({
    "sub_wallet_id": 123,
    "symbol": "ETH"
})
```

### WithdrawApi - 提现管理

```python
withdraw_api = client.get_withdraw_api()

# 发起提现
result = withdraw_api.withdraw({
    "request_id": "unique-id",
    "sub_wallet_id": 123,
    "symbol": "ETH",
    "amount": "0.1",
    "address_to": "0x1234..."
})

# 查询提现记录
records = withdraw_api.get_withdraw_records({
    "ids": [123, 456]
})

# 同步提现记录
synced = withdraw_api.sync_withdraw_records(max_id=0)
```

### DepositApi - 充值管理

```python
deposit_api = client.get_deposit_api()

# 查询充值记录
records = deposit_api.get_deposit_records({
    "ids": [123, 456, 789]
})

# 同步充值记录
synced = deposit_api.sync_deposit_records(max_id=0)
```

## 开发

### 运行测试

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 运行带覆盖率的测试
pytest --cov=chainup_custody_sdk
```

### 代码格式化

```bash
# 格式化代码
black chainup_custody_sdk tests

# 排序导入
isort chainup_custody_sdk tests

# 类型检查
mypy chainup_custody_sdk
```

## 项目结构

```
chainup_custody_sdk/
├── __init__.py          # 包导出
├── exceptions.py        # 自定义异常层次结构
├── models.py            # 数据类模型
├── enums.py             # 枚举常量
├── logger.py            # 日志工具
├── py.typed             # PEP 561 类型标记
├── utils/               # 工具模块
│   ├── crypto_provider.py
│   └── mpc_sign_util.py
├── waas/                # WaaS API 实现
│   ├── waas_client.py
│   ├── waas_config.py
│   └── api/
│       ├── base_api.py
│       ├── user_api.py
│       ├── account_api.py
│       ├── billing_api.py
│       ├── coin_api.py
│       ├── transfer_api.py
│       └── async_notify_api.py
└── mpc/                 # MPC API 实现
    ├── mpc_client.py
    ├── mpc_config.py
    └── api/
        ├── mpc_base_api.py
        ├── wallet_api.py
        ├── deposit_api.py
        ├── withdraw_api.py
        ├── workspace_api.py
        ├── auto_sweep_api.py
        ├── web3_api.py
        ├── tron_resource_api.py
        └── notify_api.py
```

## 依赖要求

- Python 3.8+
- pycryptodome >= 3.15.0
- requests >= 2.25.0

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](../LICENSE) 文件。

## 支持

- GitHub Issues: [报告问题](https://github.com/ChainUp-Custody/python-sdk/issues)
- 文档: [ChainUp Custody 文档](https://custody.chainup.com)
