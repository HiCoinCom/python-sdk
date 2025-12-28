# API Reference

This document provides detailed API reference for the ChainUp Custody Python SDK.

## Table of Contents

- [WaaS Client](#waas-client)
- [MPC Client](#mpc-client)
- [Exceptions](#exceptions)
- [Enums](#enums)
- [Models](#models)

---

## WaaS Client

### WaasClient

The main client for WaaS (Wallet-as-a-Service) API operations.

#### Constructor (Builder Pattern)

```python
from chainup_custody_sdk import WaasClient

client = (
    WaasClient.builder()
    .set_app_id("your-app-id")
    .set_private_key("your-rsa-private-key")
    .set_public_key("chainup-public-key")
    .set_debug(False)                       # optional
    .build()
)
```

#### Methods

| Method                   | Returns          | Description                            |
| ------------------------ | ---------------- | -------------------------------------- |
| `get_user_api()`         | `UserApi`        | Get user management API                |
| `get_account_api()`      | `AccountApi`     | Get account management API             |
| `get_billing_api()`      | `BillingApi`     | Get billing API                        |
| `get_coin_api()`         | `CoinApi`        | Get coin API                           |
| `get_transfer_api()`     | `TransferApi`    | Get transfer API                       |
| `get_async_notify_api()` | `AsyncNotifyApi` | Get async notification API             |
| `close()`                | `None`           | Close the client and release resources |

#### Context Manager

```python
with WaasClient.builder()...build() as client:
    # Use client
    pass
# Resources automatically released
```

---

### UserApi

User registration and management operations.

#### `register_mobile_user(params: Dict) -> Dict`

Register a new user with mobile phone.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| country | str | Yes | Country code (e.g., "86") |
| mobile | str | Yes | Mobile phone number |

**Returns:** User information with `uid`

**Example:**

```python
result = user_api.register_mobile_user({
    "country": "86",
    "mobile": "13800000000"
})
```

#### `register_email_user(params: Dict) -> Dict`

Register a new user with email.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| email | str | Yes | Email address |

**Returns:** User information with `uid`

#### `get_mobile_user(params: Dict) -> Dict`

Get user information by mobile phone.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| country | str | Yes | Country code |
| mobile | str | Yes | Mobile phone number |

#### `get_email_user(params: Dict) -> Dict`

Get user information by email.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| email | str | Yes | Email address |

#### `sync_user_list(max_id: int = 0) -> List[Dict]`

Synchronize user list with pagination.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| max_id | int | No | Starting ID for pagination (default: 0) |

---

### AccountApi

Account balance and address management.

#### `get_user_account(params: Dict) -> Dict`

Get user account balance for a cryptocurrency.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| uid | int | Yes | User ID |
| symbol | str | Yes | Cryptocurrency symbol (e.g., "BTC", "ETH") |

#### `get_user_address(params: Dict) -> Dict`

Get user deposit address.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| uid | int | Yes | User ID |
| symbol | str | Yes | Cryptocurrency symbol |

#### `get_user_address_info(params: Dict) -> Dict`

Get address information by address.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| address | str | Yes | Blockchain address |

#### `get_company_account(params: Dict) -> Dict`

Get company (merchant) account balance.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| symbol | str | Yes | Cryptocurrency symbol |

#### `sync_user_address_list(max_id: int = 0) -> List[Dict]`

Synchronize user address list.

---

### BillingApi

Deposit, withdrawal, and miner fee operations.

#### `withdraw(params: Dict) -> Dict`

Create a withdrawal request.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| request_id | str | Yes | Unique request ID |
| from_uid | int | Yes | Source user ID |
| to_address | str | Yes | Destination address |
| amount | str | Yes | Withdrawal amount |
| symbol | str | Yes | Cryptocurrency symbol |
| memo | str | No | Address memo/tag |
| remark | str | No | Additional remark |

#### `withdraw_list(ids: List[str]) -> List[Dict]`

Get withdrawal records by request IDs.

#### `sync_withdraw_list(max_id: int = 0) -> List[Dict]`

Synchronize withdrawal records.

#### `deposit_list(ids: List[str]) -> List[Dict]`

Get deposit records by WaaS IDs.

#### `sync_deposit_list(max_id: int = 0) -> List[Dict]`

Synchronize deposit records.

#### `miner_fee_list(ids: List[str]) -> List[Dict]`

Get miner fee records.

#### `sync_miner_fee_list(max_id: int = 0) -> List[Dict]`

Synchronize miner fee records.

---

### TransferApi

Internal transfer operations between users.

#### `account_transfer(params: Dict) -> Dict`

Execute internal transfer.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| request_id | str | Yes | Unique request ID |
| symbol | str | Yes | Cryptocurrency symbol |
| amount | str | Yes | Transfer amount |
| from | str | Yes | Source user ID |
| to | str | Yes | Destination user ID |
| remark | str | No | Transfer remark |

#### `get_account_transfer_list(params: Dict) -> List[Dict]`

Get transfer records.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| ids | str | Yes | Comma-separated IDs |
| ids_type | str | Yes | "request_id" or "receipt" |

#### `sync_account_transfer_list(max_id: int = 0) -> List[Dict]`

Synchronize transfer records.

---

### CoinApi

Cryptocurrency information queries.

#### `get_coin_list() -> List[Dict]`

Get list of supported cryptocurrencies.

---

### AsyncNotifyApi

Callback notification handling.

#### `notify_request(encrypted_data: str) -> Dict`

Decrypt and parse notification data.

#### `verify_request(encrypted_data: str) -> Dict`

Decrypt withdrawal verification request.

#### `verify_response(data: Dict) -> str`

Encrypt verification response.

---

## MPC Client

### MpcClient

The main client for MPC API operations.

#### Constructor (Builder Pattern)

```python
from chainup_custody_sdk import MpcClient

client = (
    MpcClient.builder()
    .set_app_id("your-app-id")
    .set_rsa_private_key("your-rsa-private-key")
    .set_sign_private_key("your-sign-private-key")  # for signing
    .set_waas_public_key("waas-public-key")
    .set_host("https://mpc.chainup.com")  # optional
    .set_debug(False)                      # optional
    .build()
)
```

#### Methods

| Method                    | Returns           | Description               |
| ------------------------- | ----------------- | ------------------------- |
| `get_wallet_api()`        | `WalletApi`       | Get wallet management API |
| `get_deposit_api()`       | `DepositApi`      | Get deposit API           |
| `get_withdraw_api()`      | `WithdrawApi`     | Get withdraw API          |
| `get_workspace_api()`     | `WorkspaceApi`    | Get workspace API         |
| `get_auto_sweep_api()`    | `AutoSweepApi`    | Get auto-sweep API        |
| `get_web3_api()`          | `Web3Api`         | Get Web3 API              |
| `get_tron_resource_api()` | `TronResourceApi` | Get TRON resource API     |
| `get_notify_api()`        | `NotifyApi`       | Get notification API      |

---

### WalletApi

MPC wallet management operations.

#### `create_wallet(params: Dict) -> Dict`

Create a new wallet.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| sub_wallet_name | str | Yes | Wallet name (max 50 chars) |
| app_show_status | int | No | 1=show, 2=hide (default) |

#### `create_wallet_address(params: Dict) -> Dict`

Create a wallet address.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| sub_wallet_id | int | Yes | Wallet ID |
| symbol | str | Yes | Coin symbol |

#### `query_wallet_address(params: Dict) -> Dict`

Query wallet addresses.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| sub_wallet_id | int | Yes | Wallet ID |
| symbol | str | Yes | Coin symbol |
| max_id | int | No | Starting ID (default: 0) |

#### `get_wallet_balance(params: Dict) -> Dict`

Get wallet balance.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| sub_wallet_id | int | Yes | Wallet ID |
| symbol | str | Yes | Coin symbol |

---

### DepositApi

Deposit record operations.

#### `get_deposit_records(params: Dict) -> Dict`

Get deposit records by IDs.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| ids | List[int] | Yes | List of deposit IDs (max 100) |

#### `sync_deposit_records(max_id: int = 0) -> Dict`

Synchronize deposit records.

---

### WithdrawApi

Withdrawal operations.

#### `withdraw(params: Dict) -> Dict`

Initiate a withdrawal.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| request_id | str | Yes | Unique request ID |
| sub_wallet_id | int | Yes | Wallet ID |
| symbol | str | Yes | Coin symbol |
| amount | str | Yes | Withdrawal amount |
| address_to | str | Yes | Destination address |
| from | str | No | Source address |
| memo | str | No | Address memo |
| remark | str | No | Remark |

#### `get_withdraw_records(params: Dict) -> Dict`

Get withdrawal records by IDs.

#### `sync_withdraw_records(max_id: int = 0) -> Dict`

Synchronize withdrawal records.

---

## Exceptions

### Exception Hierarchy

```
ChainUpError (base)
├── ApiError           # API request errors
├── ConfigError        # Configuration errors
├── CryptoError        # Encryption/decryption errors
├── NetworkError       # Network connectivity errors
├── ValidationError    # Input validation errors
├── SignatureError     # Signature verification errors
├── AuthenticationError # Authentication errors
└── RateLimitError     # Rate limiting errors
```

### ChainUpError

Base exception for all SDK errors.

**Attributes:**
| Name | Type | Description |
|------|------|-------------|
| message | str | Error message |
| code | int | Error code (optional) |
| details | Dict | Additional details (optional) |

### ApiError

API request errors with additional context.

**Attributes:**
| Name | Type | Description |
|------|------|-------------|
| message | str | Error message |
| code | int | API error code |
| http_status | int | HTTP status code (optional) |
| request_id | str | Request ID for tracking (optional) |

---

## Enums

### ApiCode

API response codes.

```python
from chainup_custody_sdk import ApiCode

ApiCode.SUCCESS           # 0
ApiCode.SYSTEM_ERROR      # 100001
ApiCode.PARAM_INVALID     # 100004
ApiCode.SIGN_ERROR        # 100005
ApiCode.IP_FORBIDDEN      # 100007
# ... see full list in code
```

### MpcDepositStatus

Deposit transaction status.

```python
from chainup_custody_sdk import MpcDepositStatus

MpcDepositStatus.CONFIRMING  # 1900
MpcDepositStatus.SUCCESS     # 2000
MpcDepositStatus.FAILED      # 2400
```

### MpcWithdrawStatus

Withdrawal transaction status.

```python
from chainup_custody_sdk import MpcWithdrawStatus

MpcWithdrawStatus.PENDING_AUDIT    # 1000
MpcWithdrawStatus.AUDIT_PASSED     # 1100
MpcWithdrawStatus.AUDIT_REJECTED   # 2300
MpcWithdrawStatus.PROCESSING       # 1200
MpcWithdrawStatus.SUCCESS          # 2000
MpcWithdrawStatus.FAILED           # 2400
MpcWithdrawStatus.CANCELLED        # 2200
```

---

## Models

### ApiResponse

Generic API response wrapper.

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

Wallet information dataclass.

**Attributes:**
| Name | Type | Description |
|------|------|-------------|
| sub_wallet_id | int | Wallet ID |
| sub_wallet_name | str | Wallet name |
| symbol | str | Cryptocurrency symbol |
| address | str | Wallet address |

### TransactionRecord

Transaction record dataclass.

**Attributes:**
| Name | Type | Description |
|------|------|-------------|
| id | int | Transaction ID |
| request_id | str | Request ID |
| symbol | str | Cryptocurrency symbol |
| amount | str | Transaction amount |
| address | str | Address |
| status | TransactionStatus | Transaction status |
| side | TransactionSide | Transaction side (deposit/withdraw) |
| tx_hash | str | Transaction hash (optional) |
| created_at | str | Creation time (optional) |

### NotifyData

Callback notification data.

**Attributes:**
| Name | Type | Description |
|------|------|-------------|
| id | int | Notification ID |
| uid | int | User ID |
| symbol | str | Cryptocurrency symbol |
| amount | str | Amount |
| address | str | Address |
| tx_hash | str | Transaction hash |
| notify_type | str | "deposit" or "withdraw" |
| status | int | Transaction status |
