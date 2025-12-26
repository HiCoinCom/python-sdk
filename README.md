# ChainUp Custody Python SDK

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.1.0-orange.svg)](https://github.com/ChainUp-Custody/python-sdk)

A comprehensive Python SDK for ChainUp Custody's WaaS (Wallet-as-a-Service) and MPC (Multi-Party Computation) APIs.

**[中文文档](README_CN.md)**

## Features

- 🔐 **WaaS API** - Wallet-as-a-Service for managing users, accounts, deposits, and withdrawals
- 🔑 **MPC API** - Multi-Party Computation for secure wallet management
- 📝 **Type Hints** - Full type annotations for better IDE support
- 🛡️ **Custom Exceptions** - Detailed error handling with specific exception types
- 📊 **Data Models** - Dataclass-based models for type-safe data handling
- 🔧 **Builder Pattern** - Fluent API for easy client configuration
- 🪵 **Logging** - Configurable logging system
- ✅ **Tested** - Comprehensive unit test coverage

## Installation

### From Source

```bash
git clone https://github.com/ChainUp-Custody/python-sdk.git
cd python-sdk
pip install -e .
```

### Using pip (coming soon)

```bash
pip install chainup-custody-sdk
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Quick Start

### WaaS Client

```python
from chainup_custody_sdk import WaasClient, ApiError

# Create client using builder pattern
client = (
    WaasClient.builder()
    .set_app_id("your-app-id")
    .set_private_key("your-rsa-private-key")
    .set_public_key("chainup-public-key")
    .set_debug(False)
    .build()
)

# Use context manager for automatic resource cleanup
with client:
    # Register a user
    try:
        user = client.get_user_api().register_email_user({
            "email": "user@example.com"
        })
        print(f"User created: {user}")
    except ApiError as e:
        print(f"API Error: {e}")

    # Get account balance
    balance = client.get_account_api().get_user_account({
        "uid": 12345,
        "symbol": "ETH"
    })
    print(f"Balance: {balance}")
```

### MPC Client

```python
from chainup_custody_sdk import MpcClient, ApiError

# Create MPC client
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
    # Create a wallet
    try:
        wallet = client.get_wallet_api().create_wallet({
            "sub_wallet_name": "My Wallet",
            "app_show_status": 1
        })
        print(f"Wallet created: {wallet}")
    except ApiError as e:
        print(f"Error: {e}")

    # Query deposits
    deposits = client.get_deposit_api().sync_deposit_records(0)
    print(f"Deposits: {deposits}")
```

## API Reference

### WaaS APIs

| API              | Description                            |
| ---------------- | -------------------------------------- |
| `UserApi`        | User registration and management       |
| `AccountApi`     | Account balance and address management |
| `BillingApi`     | Deposits, withdrawals, and miner fees  |
| `CoinApi`        | Cryptocurrency list queries            |
| `TransferApi`    | Internal transfers between users       |
| `AsyncNotifyApi` | Callback notification handling         |

### MPC APIs

| API               | Description                    |
| ----------------- | ------------------------------ |
| `WalletApi`       | Wallet creation and management |
| `DepositApi`      | Deposit record queries         |
| `WithdrawApi`     | Withdrawal operations          |
| `WorkspaceApi`    | Workspace and chain management |
| `AutoSweepApi`    | Auto-sweep configuration       |
| `Web3Api`         | Web3 contract interactions     |
| `TronResourceApi` | TRON resource management       |
| `NotifyApi`       | MPC callback handling          |

## Error Handling

The SDK provides a hierarchy of custom exceptions:

```python
from chainup_custody_sdk import (
    ChainUpError,      # Base exception
    ApiError,          # API request errors
    ConfigError,       # Configuration errors
    CryptoError,       # Encryption/decryption errors
    NetworkError,      # Network connectivity errors
    ValidationError,   # Input validation errors
    SignatureError,    # Signature verification errors
    RateLimitError,    # Rate limiting errors
)

try:
    result = client.get_billing_api().withdraw({...})
except ApiError as e:
    print(f"API Error [{e.code}]: {e.message}")
except ConfigError as e:
    print(f"Configuration Error: {e}")
except ChainUpError as e:
    print(f"SDK Error: {e}")
```

## API Error Codes

| Code    | Constant                  | Description                            |
| ------- | ------------------------- | -------------------------------------- |
| 0       | `SUCCESS`                 | Success                                |
| 100001  | `SYSTEM_ERROR`            | System error                           |
| 100004  | `PARAM_INVALID`           | Invalid request parameters             |
| 100005  | `SIGN_ERROR`              | Signature verification failed          |
| 100007  | `IP_FORBIDDEN`            | IP address not allowed                 |
| 100015  | `MERCHANT_ID_INVALID`     | Invalid merchant ID                    |
| 100016  | `MERCHANT_EXPIRED`        | Merchant information expired           |
| 110004  | `USER_FROZEN`             | User is frozen, withdrawal not allowed |
| 110023  | `MOBILE_REGISTERED`       | Mobile number already registered       |
| 110037  | `WITHDRAW_ADDRESS_RISK`   | Withdrawal address has risk            |
| 110055  | `WITHDRAW_ADDRESS_ERROR`  | Invalid withdrawal address             |
| 110065  | `USER_NOT_EXIST`          | User does not exist                    |
| 110078  | `AMOUNT_BELOW_MIN`        | Amount below minimum                   |
| 110087  | `AMOUNT_EXCEED_MAX`       | Amount exceeds maximum                 |
| 110088  | `DUPLICATE_REQUEST`       | Duplicate request                      |
| 120202  | `COIN_NOT_SUPPORTED`      | Coin not supported                     |
| 120402  | `BALANCE_INSUFFICIENT`    | Insufficient balance                   |
| 120403  | `FEE_INSUFFICIENT`        | Insufficient fee balance               |
| 3040006 | `SELF_TRANSFER_FORBIDDEN` | Cannot transfer to self                |

## Logging

Configure logging for debugging:

```python
from chainup_custody_sdk import configure_logging, enable_debug_logging

# Enable debug logging
enable_debug_logging()

# Or configure with custom settings
configure_logging(level="DEBUG", format="%(asctime)s - %(name)s - %(message)s")
```

## Data Models

The SDK provides dataclass-based models:

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

# Parse API response
response = ApiResponse.from_dict(api_data)
if response.is_success:
    wallet = WalletInfo.from_dict(response.data)
    print(f"Wallet ID: {wallet.sub_wallet_id}")
```

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=chainup_custody_sdk
```

### Code Formatting

```bash
# Format code
black chainup_custody_sdk tests

# Sort imports
isort chainup_custody_sdk tests

# Type checking
mypy chainup_custody_sdk
```

## Project Structure

```
chainup_custody_sdk/
├── __init__.py          # Package exports
├── exceptions.py        # Custom exception hierarchy
├── models.py            # Dataclass models
├── enums.py             # Enum constants
├── logger.py            # Logging utilities
├── py.typed             # PEP 561 type marker
├── utils/               # Utility modules
│   ├── crypto_provider.py
│   └── mpc_sign_util.py
├── waas/                # WaaS API implementation
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
└── mpc/                 # MPC API implementation
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

## Requirements

- Python 3.8+
- pycryptodome >= 3.15.0
- requests >= 2.25.0

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## Support

- GitHub Issues: [Report a bug](https://github.com/ChainUp-Custody/python-sdk/issues)
- Documentation: [ChainUp Custody Docs](https://custody.chainup.com)
