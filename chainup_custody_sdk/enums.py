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


class MpcDepositStatus(IntEnum):
    """Deposit transaction status."""
    CONFIRMING = 1900
    SUCCESS = 2000
    FAILED = 2400


class MpcWithdrawStatus(IntEnum):
    """Withdrawal transaction status."""
    PENDING_AUDIT = 1000
    AUDIT_PASSED = 1100
    AUDIT_REJECTED = 2300
    PROCESSING = 1200
    SUCCESS = 2000
    FAILED = 2400
    CANCELLED = 2200


class MpcWeb3TransType(IntEnum):
    """Web3 transaction types."""
    APPROVE = 0
    TRANSACTION = 1
    TRON_PERMISSION_APPROVE = 22
    TRON_APPROVED_TRANSFER = 23


class TronResourceType(IntEnum):
    """TRON resource types for delegation."""
    BANDWIDTH_AND_ENERGY = 0
    ENERGY = 1


class TronServiceType(str, Enum):
    """TRON resource service duration types."""
    TEN_MIN = "10010"
    ONE_HOUR = "20001"
    ONE_DAY = "30001"
    

class TronBuyType(IntEnum):
    """TRON resource buy types."""
    SYSTEM = 0
    MANUAL = 1


class WalletShowStatus(IntEnum):
    """Wallet display status in app."""
    HIDDEN = 2
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
