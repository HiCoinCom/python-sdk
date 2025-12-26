"""
ChainUp Custody Python SDK

A comprehensive Python SDK for ChainUp Custody's WaaS (Wallet-as-a-Service) 
and MPC (Multi-Party Computation) APIs.

Author: ChainUp Custody
Version: 1.1.0
License: MIT

Example:
    # WaaS Client
    from chainup_custody_sdk import WaasClient
    
    client = (
        WaasClient.builder()
        .set_app_id("your-app-id")
        .set_private_key("your-private-key")
        .set_public_key("chainup-public-key")
        .build()
    )
    
    # MPC Client
    from chainup_custody_sdk import MpcClient
    
    client = (
        MpcClient.builder()
        .set_app_id("your-app-id")
        .set_rsa_private_key("your-private-key")
        .set_waas_public_key("waas-public-key")
        .build()
    )
"""
from __future__ import annotations

# Core clients
from chainup_custody_sdk.waas.waas_client import WaasClient
from chainup_custody_sdk.waas.waas_config import WaasConfig
from chainup_custody_sdk.mpc.mpc_client import MpcClient
from chainup_custody_sdk.mpc.mpc_config import MpcConfig

# Crypto utilities
from chainup_custody_sdk.utils.crypto_provider import ICryptoProvider, RsaCryptoProvider
from chainup_custody_sdk.utils.mpc_sign_util import MpcSignUtil

# Exceptions
from chainup_custody_sdk.exceptions import (
    ChainUpError,
    ApiError,
    ConfigError,
    CryptoError,
    NetworkError,
    ValidationError,
    SignatureError,
    AuthenticationError,
    RateLimitError,
)

# Enums
from chainup_custody_sdk.enums import (
    HttpMethod,
    ApiCode,
    DepositStatus,
    WithdrawStatus,
    Web3TransType,
    TronResourceType,
    QueryIdType,
)

# Models
from chainup_custody_sdk.models import (
    ApiResponse,
    WalletInfo,
    AddressInfo,
    TransactionRecord,
    CoinInfo,
    UserInfo,
    NotifyData,
    AssetBalance,
    TransactionStatus,
    TransactionSide,
)

# Logging utilities
from chainup_custody_sdk.logger import (
    get_logger,
    configure_logging,
    enable_debug_logging,
    disable_logging,
)

__version__ = "1.1.0"
__author__ = "ChainUp Custody"

__all__ = [
    # Version info
    "__version__",
    "__author__",
    # Core clients
    "WaasClient",
    "WaasConfig",
    "MpcClient",
    "MpcConfig",
    # Crypto
    "ICryptoProvider",
    "RsaCryptoProvider",
    "MpcSignUtil",
    # Exceptions
    "ChainUpError",
    "ApiError",
    "ConfigError",
    "CryptoError",
    "NetworkError",
    "ValidationError",
    "SignatureError",
    "AuthenticationError",
    "RateLimitError",
    # Enums
    "HttpMethod",
    "ApiCode",
    "DepositStatus",
    "WithdrawStatus",
    "Web3TransType",
    "TronResourceType",
    "QueryIdType",
    # Models
    "ApiResponse",
    "WalletInfo",
    "AddressInfo",
    "TransactionRecord",
    "CoinInfo",
    "UserInfo",
    "NotifyData",
    "AssetBalance",
    "TransactionStatus",
    "TransactionSide",
    # Logging
    "get_logger",
    "configure_logging",
    "enable_debug_logging",
    "disable_logging",
]
