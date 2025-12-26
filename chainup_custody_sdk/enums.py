"""
ChainUp Custody SDK Enumerations

Defines enums for constants used throughout the SDK.
"""
from enum import Enum, IntEnum


class HttpMethod(str, Enum):
    """HTTP request methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class ApiCode(IntEnum):
    """API response codes."""
    # Success
    SUCCESS = 0
    
    # System errors
    SYSTEM_ERROR = 100001  # System error
    PARAM_INVALID = 100004  # Invalid request parameters (withdrawal confirmation callback failed)
    SIGN_ERROR = 100005  # Signature verification failed
    IP_FORBIDDEN = 100007  # IP address not allowed
    MERCHANT_ID_INVALID = 100015  # Invalid merchant ID
    MERCHANT_EXPIRED = 100016  # Merchant information expired
    
    # User-related errors
    USER_FROZEN = 110004  # User is frozen, withdrawal not allowed
    MOBILE_REGISTERED = 110023  # Mobile number already registered
    WITHDRAW_ADDRESS_RISK = 110037  # Withdrawal address has risk
    WITHDRAW_ADDRESS_ERROR = 110055  # Invalid withdrawal address
    USER_NOT_EXIST = 110065  # User does not exist (used for balance query, withdrawal or transfer)
    AMOUNT_BELOW_MIN = 110078  # Withdrawal or transfer amount below minimum
    AMOUNT_EXCEED_MAX = 110087  # Withdrawal or transfer amount exceeds maximum
    DUPLICATE_REQUEST = 110088  # Duplicate request, please do not resubmit
    MOBILE_INVALID = 110089  # Invalid mobile number for registration
    REGISTER_FAILED = 110101  # User registration failed
    PRECISION_EXCEEDED = 110161  # Withdrawal precision exceeded maximum supported
    
    # Coin/transaction-related errors
    COIN_NOT_SUPPORTED = 120202  # Coin not supported
    CONFIRM_FAILED = 120206  # Withdrawal confirmation failed
    BALANCE_INSUFFICIENT = 120402  # Insufficient balance for withdrawal or transfer
    FEE_INSUFFICIENT = 120403  # Insufficient balance for withdrawal fee
    AMOUNT_LESS_THAN_FEE = 120404  # Withdrawal or transfer amount too small, less than or equal to fee
    
    # Risk control errors
    USER_RISK_FORBIDDEN = 900006  # User has risk, withdrawal forbidden
    
    # Transfer-related errors
    SELF_TRANSFER_FORBIDDEN = 3040006  # Cannot transfer to self


class DepositStatus(IntEnum):
    """Deposit transaction status."""
    CONFIRMING = 0
    SUCCESS = 1
    FAILED = 2


class WithdrawStatus(IntEnum):
    """Withdrawal transaction status."""
    PENDING_AUDIT = 0
    AUDITING = 1
    AUDIT_PASSED = 2
    AUDIT_REJECTED = 3
    PROCESSING = 4
    BROADCASTING = 5
    SUCCESS = 6
    FAILED = 7
    CANCELLED = 8


class Web3TransType(IntEnum):
    """Web3 transaction types."""
    CONTRACT_CALL = 1
    CONTRACT_DEPLOY = 2
    TRANSFER = 3


class TronResourceType(IntEnum):
    """TRON resource types for delegation."""
    ENERGY = 1
    BANDWIDTH = 2


class TronBuyType(IntEnum):
    """TRON resource buy types."""
    API_BUY = 0
    MANUAL = 1


class WalletShowStatus(IntEnum):
    """Wallet display status in app."""
    HIDDEN = 0
    VISIBLE = 1


class AutoCollectStatus(IntEnum):
    """Auto-collection status."""
    DISABLED = 0
    ENABLED = 1


class QueryIdType(str, Enum):
    """ID type for querying records."""
    REQUEST_ID = "request_id"
    RECEIPT = "receipt"
    WAAS_ID = "id"


class CoinType(str, Enum):
    """Cryptocurrency type."""
    MAIN_COIN = "main"
    TOKEN = "token"


class NetworkType(str, Enum):
    """Blockchain network type."""
    MAINNET = "mainnet"
    TESTNET = "testnet"


class ContentType(str, Enum):
    """HTTP Content-Type headers."""
    FORM = "application/x-www-form-urlencoded"
    JSON = "application/json"
    MULTIPART = "multipart/form-data"


class Charset(str, Enum):
    """Character encoding."""
    UTF8 = "UTF-8"
    ASCII = "ASCII"
    LATIN1 = "ISO-8859-1"
