"""
ChainUp Custody Python SDK
Main entry point for WaaS (Wallet-as-a-Service) and MPC (Multi-Party Computation) APIs

Author: ChainUp Custody
Version: 1.0.0
License: MIT
"""

from chainup_custody_sdk.waas.waas_client import WaasClient
from chainup_custody_sdk.waas.waas_config import WaasConfig
from chainup_custody_sdk.mpc.mpc_client import MpcClient
from chainup_custody_sdk.mpc.mpc_config import MpcConfig
from chainup_custody_sdk.utils.crypto_provider import ICryptoProvider, RsaCryptoProvider
from chainup_custody_sdk.utils.mpc_sign_util import MpcSignUtil

__version__ = "1.0.0"
__author__ = "ChainUp Custody"
__all__ = [
    "WaasClient",
    "WaasConfig",
    "MpcClient",
    "MpcConfig",
    "ICryptoProvider",
    "RsaCryptoProvider",
    "MpcSignUtil",
]
