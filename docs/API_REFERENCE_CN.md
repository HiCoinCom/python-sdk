# API 参考文档

本文档提供 ChainUp Custody Python SDK 的详细 API 参考。

## 目录

- [WaaS 客户端](#waas-客户端)
- [MPC 客户端](#mpc-客户端)
- [异常](#异常)
- [枚举](#枚举)
- [数据模型](#数据模型)

---

## WaaS 客户端

### WaasClient

WaaS（钱包即服务）API 操作的主客户端。

#### 构造器（Builder 模式）

```python
from chainup_custody_sdk import WaasClient

client = (
    WaasClient.builder()
    .set_app_id("your-app-id")
    .set_private_key("your-rsa-private-key")
    .set_public_key("chainup-public-key")
    .set_debug(False)                       # 可选
    .build()
)
```

#### 方法

| 方法                     | 返回值           | 描述                 |
| ------------------------ | ---------------- | -------------------- |
| `get_user_api()`         | `UserApi`        | 获取用户管理 API     |
| `get_account_api()`      | `AccountApi`     | 获取账户管理 API     |
| `get_billing_api()`      | `BillingApi`     | 获取账单 API         |
| `get_coin_api()`         | `CoinApi`        | 获取币种 API         |
| `get_transfer_api()`     | `TransferApi`    | 获取转账 API         |
| `get_async_notify_api()` | `AsyncNotifyApi` | 获取异步通知 API     |
| `close()`                | `None`           | 关闭客户端并释放资源 |

#### 上下文管理器

```python
with WaasClient.builder()...build() as client:
    # 使用客户端
    pass
# 资源自动释放
```

---

### UserApi

用户注册和管理操作。

#### `register_mobile_user(params: Dict) -> Dict`

使用手机号注册新用户。

**参数:**
| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| country | str | 是 | 国家代码（如 "86"） |
| mobile | str | 是 | 手机号码 |

**返回:** 包含 `uid` 的用户信息

**示例:**

```python
result = user_api.register_mobile_user({
    "country": "86",
    "mobile": "13800000000"
})
```

#### `register_email_user(params: Dict) -> Dict`

使用邮箱注册新用户。

**参数:**
| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| email | str | 是 | 邮箱地址 |

**返回:** 包含 `uid` 的用户信息

#### `get_mobile_user(params: Dict) -> Dict`

通过手机号获取用户信息。

**参数:**
| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| country | str | 是 | 国家代码 |
| mobile | str | 是 | 手机号码 |

#### `get_email_user(params: Dict) -> Dict`

通过邮箱获取用户信息。

**参数:**
| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| email | str | 是 | 邮箱地址 |

#### `sync_user_list(max_id: int = 0) -> List[Dict]`

分页同步用户列表。

**参数:**
| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| max_id | int | 否 | 分页起始 ID（默认: 0） |

---

### AccountApi

账户余额和地址管理。

#### `get_user_account(params: Dict) -> Dict`

获取用户某个加密货币的账户余额。

**参数:**
| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| uid | int | 是 | 用户 ID |
| symbol | str | 是 | 加密货币符号（如 "BTC", "ETH"） |

#### `get_user_address(params: Dict) -> Dict`

获取用户充值地址。

**参数:**
| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| uid | int | 是 | 用户 ID |
| symbol | str | 是 | 加密货币符号 |

#### `get_user_address_info(params: Dict) -> Dict`

通过地址获取地址信息。

**参数:**
| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| address | str | 是 | 区块链地址 |

#### `get_company_account(params: Dict) -> Dict`

获取公司（商户）账户余额。

**参数:**
| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| symbol | str | 是 | 加密货币符号 |

#### `sync_user_address_list(max_id: int = 0) -> List[Dict]`

同步用户地址列表。

---

### BillingApi

充值、提现和矿工费操作。

#### `withdraw(params: Dict) -> Dict`

创建提现请求。

**参数:**
| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| request_id | str | 是 | 唯一请求 ID |
| from_uid | int | 是 | 源用户 ID |
| to_address | str | 是 | 目标地址 |
| amount | str | 是 | 提现金额 |
| symbol | str | 是 | 加密货币符号 |
| memo | str | 否 | 地址备注/标签 |
| remark | str | 否 | 附加备注 |

#### `withdraw_list(ids: List[str]) -> List[Dict]`

通过请求 ID 获取提现记录。

#### `sync_withdraw_list(max_id: int = 0) -> List[Dict]`

同步提现记录。

#### `deposit_list(ids: List[str]) -> List[Dict]`

通过 WaaS ID 获取充值记录。

#### `sync_deposit_list(max_id: int = 0) -> List[Dict]`

同步充值记录。

#### `miner_fee_list(ids: List[str]) -> List[Dict]`

获取矿工费记录。

#### `sync_miner_fee_list(max_id: int = 0) -> List[Dict]`

同步矿工费记录。

---

### TransferApi

用户间内部转账操作。

#### `account_transfer(params: Dict) -> Dict`

执行内部转账。

**参数:**
| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| request_id | str | 是 | 唯一请求 ID |
| symbol | str | 是 | 加密货币符号 |
| amount | str | 是 | 转账金额 |
| from | str | 是 | 源用户 ID |
| to | str | 是 | 目标用户 ID |
| remark | str | 否 | 转账备注 |

#### `get_account_transfer_list(params: Dict) -> List[Dict]`

获取转账记录。

**参数:**
| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| ids | str | 是 | 逗号分隔的 ID |
| ids_type | str | 是 | "request_id" 或 "receipt" |

#### `sync_account_transfer_list(max_id: int = 0) -> List[Dict]`

同步转账记录。

---

### CoinApi

加密货币信息查询。

#### `get_coin_list() -> List[Dict]`

获取支持的加密货币列表。

---

### AsyncNotifyApi

回调通知处理。

#### `notify_request(encrypted_data: str) -> Dict`

解密并解析通知数据。

#### `verify_request(encrypted_data: str) -> Dict`

解密提现验证请求。

#### `verify_response(data: Dict) -> str`

加密验证响应。

---

## MPC 客户端

### MpcClient

MPC API 操作的主客户端。

#### 构造器（Builder 模式）

```python
from chainup_custody_sdk import MpcClient

client = (
    MpcClient.builder()
    .set_app_id("your-app-id")
    .set_rsa_private_key("your-rsa-private-key")
    .set_sign_private_key("your-sign-private-key")  # 用于签名
    .set_waas_public_key("waas-public-key")
    .set_debug(False)                      # 可选
    .build()
)
```

#### 方法

| 方法                      | 返回值            | 描述               |
| ------------------------- | ----------------- | ------------------ |
| `get_wallet_api()`        | `WalletApi`       | 获取钱包管理 API   |
| `get_deposit_api()`       | `DepositApi`      | 获取充值 API       |
| `get_withdraw_api()`      | `WithdrawApi`     | 获取提现 API       |
| `get_workspace_api()`     | `WorkspaceApi`    | 获取工作空间 API   |
| `get_auto_sweep_api()`    | `AutoSweepApi`    | 获取自动归集 API   |
| `get_web3_api()`          | `Web3Api`         | 获取 Web3 API      |
| `get_tron_resource_api()` | `TronResourceApi` | 获取 TRON 资源 API |
| `get_notify_api()`        | `NotifyApi`       | 获取通知 API       |

---

### WalletApi

MPC 钱包管理操作。

#### `create_wallet(params: Dict) -> Dict`

创建新钱包。

**参数:**
| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| sub_wallet_name | str | 是 | 钱包名称（最多 50 字符） |
| app_show_status | int | 否 | 1=显示, 2=隐藏（默认） |

#### `create_wallet_address(params: Dict) -> Dict`

创建钱包地址。

**参数:**
| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| sub_wallet_id | int | 是 | 钱包 ID |
| symbol | str | 是 | 币种符号 |

#### `query_wallet_address(params: Dict) -> Dict`

查询钱包地址。

**参数:**
| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| sub_wallet_id | int | 是 | 钱包 ID |
| symbol | str | 是 | 币种符号 |
| max_id | int | 否 | 起始 ID（默认: 0） |

#### `get_wallet_balance(params: Dict) -> Dict`

获取钱包余额。

**参数:**
| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| sub_wallet_id | int | 是 | 钱包 ID |
| symbol | str | 是 | 币种符号 |

---

### DepositApi

充值记录操作。

#### `get_deposit_records(params: Dict) -> Dict`

通过 ID 获取充值记录。

**参数:**
| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| ids | List[int] | 是 | 充值 ID 列表（最多 100 个） |

#### `sync_deposit_records(max_id: int = 0) -> Dict`

同步充值记录。

---

### WithdrawApi

提现操作。

#### `withdraw(params: Dict) -> Dict`

发起提现。

**参数:**
| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| request_id | str | 是 | 唯一请求 ID |
| sub_wallet_id | int | 是 | 钱包 ID |
| symbol | str | 是 | 币种符号 |
| amount | str | 是 | 提现金额 |
| address_to | str | 是 | 目标地址 |
| from | str | 否 | 源地址 |
| memo | str | 否 | 地址备注 |
| remark | str | 否 | 备注 |

#### `get_withdraw_records(params: Dict) -> Dict`

通过 ID 获取提现记录。

#### `sync_withdraw_records(max_id: int = 0) -> Dict`

同步提现记录。

---

## 异常

### 异常层次结构

```
ChainUpError (基类)
├── ApiError           # API 请求错误
├── ConfigError        # 配置错误
├── CryptoError        # 加密/解密错误
├── NetworkError       # 网络连接错误
├── ValidationError    # 输入验证错误
├── SignatureError     # 签名验证错误
├── AuthenticationError # 认证错误
└── RateLimitError     # 限流错误
```

### ChainUpError

所有 SDK 错误的基础异常。

**属性:**
| 名称 | 类型 | 描述 |
|------|------|------|
| message | str | 错误消息 |
| code | int | 错误代码（可选） |
| details | Dict | 附加详情（可选） |

### ApiError

带有附加上下文的 API 请求错误。

**属性:**
| 名称 | 类型 | 描述 |
|------|------|------|
| message | str | 错误消息 |
| code | int | API 错误代码 |
| http_status | int | HTTP 状态码（可选） |
| request_id | str | 请求 ID，用于追踪（可选） |

---

## 枚举

### ApiCode

API 响应代码。

```python
from chainup_custody_sdk import ApiCode

ApiCode.SUCCESS           # 0 - 成功
ApiCode.SYSTEM_ERROR      # 100001 - 系统错误
ApiCode.PARAM_INVALID     # 100004 - 请求参数不合法
ApiCode.SIGN_ERROR        # 100005 - 签名校验失败
ApiCode.IP_FORBIDDEN      # 100007 - 非法IP
ApiCode.MERCHANT_ID_INVALID  # 100015 - 商户ID无效
ApiCode.MERCHANT_EXPIRED  # 100016 - 商户信息过期
ApiCode.USER_FROZEN       # 110004 - 用户被冻结不可提现
ApiCode.MOBILE_REGISTERED # 110023 - 手机号已注册
ApiCode.WITHDRAW_ADDRESS_RISK  # 110037 - 提现地址存在风险
ApiCode.WITHDRAW_ADDRESS_ERROR # 110055 - 提现地址错误
ApiCode.USER_NOT_EXIST    # 110065 - 用户不存在
ApiCode.AMOUNT_BELOW_MIN  # 110078 - 金额小于最小转出金额
ApiCode.AMOUNT_EXCEED_MAX # 110087 - 金额大于最大转出金额
ApiCode.DUPLICATE_REQUEST # 110088 - 请勿重复提交请求
ApiCode.MOBILE_INVALID    # 110089 - 注册手机号不正确
ApiCode.REGISTER_FAILED   # 110101 - 用户注册失败
ApiCode.PRECISION_EXCEEDED # 110161 - 超过提现最大支持精度
ApiCode.COIN_NOT_SUPPORTED # 120202 - 币种不支持
ApiCode.CONFIRM_FAILED    # 120206 - 提现二次确认失败
ApiCode.BALANCE_INSUFFICIENT  # 120402 - 余额不足
ApiCode.FEE_INSUFFICIENT  # 120403 - 手续费余额不足
ApiCode.AMOUNT_LESS_THAN_FEE  # 120404 - 金额小于等于手续费
ApiCode.USER_RISK_FORBIDDEN   # 900006 - 用户存在风险，禁止提现
ApiCode.SELF_TRANSFER_FORBIDDEN  # 3040006 - 不能给自己转账
```

### DepositStatus

充值交易状态。

```python
from chainup_custody_sdk import DepositStatus

DepositStatus.CONFIRMING  # 0 - 确认中
DepositStatus.SUCCESS     # 1 - 成功
DepositStatus.FAILED      # 2 - 失败
```

### WithdrawStatus

提现交易状态。

```python
from chainup_custody_sdk import WithdrawStatus

WithdrawStatus.PENDING_AUDIT    # 0 - 待审核
WithdrawStatus.AUDITING         # 1 - 审核中
WithdrawStatus.AUDIT_PASSED     # 2 - 审核通过
WithdrawStatus.AUDIT_REJECTED   # 3 - 审核拒绝
WithdrawStatus.PROCESSING       # 4 - 处理中
WithdrawStatus.BROADCASTING     # 5 - 广播中
WithdrawStatus.SUCCESS          # 6 - 成功
WithdrawStatus.FAILED           # 7 - 失败
WithdrawStatus.CANCELLED        # 8 - 已取消
```

---

## 数据模型

### ApiResponse

通用 API 响应包装器。

```python
from chainup_custody_sdk import ApiResponse

response = ApiResponse.from_dict({
    "code": 0,
    "msg": "success",
    "data": {...}
})

if response.is_success:
    print(response.data)
```

### WalletInfo

钱包信息数据类。

**属性:**
| 名称 | 类型 | 描述 |
|------|------|------|
| sub_wallet_id | int | 钱包 ID |
| sub_wallet_name | str | 钱包名称 |
| symbol | str | 加密货币符号 |
| address | str | 钱包地址 |

### TransactionRecord

交易记录数据类。

**属性:**
| 名称 | 类型 | 描述 |
|------|------|------|
| id | int | 交易 ID |
| request_id | str | 请求 ID |
| symbol | str | 加密货币符号 |
| amount | str | 交易金额 |
| address | str | 地址 |
| status | TransactionStatus | 交易状态 |
| side | TransactionSide | 交易方向（充值/提现） |
| tx_hash | str | 交易哈希（可选） |
| created_at | str | 创建时间（可选） |

### NotifyData

回调通知数据。

**属性:**
| 名称 | 类型 | 描述 |
|------|------|------|
| id | int | 通知 ID |
| uid | int | 用户 ID |
| symbol | str | 加密货币符号 |
| amount | str | 金额 |
| address | str | 地址 |
| tx_hash | str | 交易哈希 |
| notify_type | str | "deposit" 或 "withdraw" |
| status | int | 交易状态 |
