"""
ChainUp Custody SDK Data Models

Defines data classes for configuration, responses, and domain objects.
Uses dataclasses for clean, type-safe data structures.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum


class TransactionStatus(Enum):
    """Transaction status enumeration."""
    PENDING = 0
    PROCESSING = 1
    SUCCESS = 2
    FAILED = 3
    CANCELLED = 4


class TransactionSide(Enum):
    """Transaction side (direction) enumeration."""
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    TRANSFER = "transfer"


class ResourceType(Enum):
    """TRON resource type enumeration."""
    ENERGY = 1
    BANDWIDTH = 2


@dataclass
class ApiResponse:
    """
    Generic API response wrapper.
    
    Attributes:
        code: Response code (0 = success)
        msg: Response message
        data: Response data payload
    """
    code: int
    msg: str
    data: Optional[Any] = None
    
    @property
    def is_success(self) -> bool:
        """Check if response indicates success."""
        return self.code == 0
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ApiResponse":
        """Create ApiResponse from dictionary."""
        return cls(
            code=data.get("code", -1),
            msg=data.get("msg", ""),
            data=data.get("data")
        )


@dataclass
class WalletInfo:
    """
    Wallet information.
    
    Attributes:
        sub_wallet_id: Sub-wallet ID
        sub_wallet_name: Sub-wallet name
        symbol: Cryptocurrency symbol
        address: Wallet address
    """
    sub_wallet_id: int
    sub_wallet_name: str = ""
    symbol: str = ""
    address: str = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WalletInfo":
        """Create WalletInfo from dictionary."""
        return cls(
            sub_wallet_id=data.get("sub_wallet_id", 0),
            sub_wallet_name=data.get("sub_wallet_name", ""),
            symbol=data.get("symbol", ""),
            address=data.get("address", "")
        )


@dataclass
class AddressInfo:
    """
    Address information.
    
    Attributes:
        id: Address ID
        uid: User ID
        address: Blockchain address
        symbol: Cryptocurrency symbol
        memo: Address memo/tag (optional)
    """
    id: int
    uid: int
    address: str
    symbol: str
    memo: str = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AddressInfo":
        """Create AddressInfo from dictionary."""
        return cls(
            id=data.get("id", 0),
            uid=data.get("uid", 0),
            address=data.get("address", ""),
            symbol=data.get("symbol", ""),
            memo=data.get("memo", "")
        )


@dataclass
class TransactionRecord:
    """
    Transaction record.
    
    Attributes:
        id: Transaction ID
        request_id: Merchant request ID
        symbol: Cryptocurrency symbol
        amount: Transaction amount
        address_from: Source address
        address_to: Destination address
        txid: Blockchain transaction hash
        status: Transaction status
        confirm_count: Confirmation count
        created_at: Creation timestamp
    """
    id: int
    request_id: str
    symbol: str
    amount: str
    address_from: str = ""
    address_to: str = ""
    txid: str = ""
    status: int = 0
    confirm_count: int = 0
    created_at: int = 0
    
    @property
    def transaction_status(self) -> TransactionStatus:
        """Get transaction status as enum."""
        try:
            return TransactionStatus(self.status)
        except ValueError:
            return TransactionStatus.PENDING
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TransactionRecord":
        """Create TransactionRecord from dictionary."""
        return cls(
            id=data.get("id", 0),
            request_id=data.get("request_id", ""),
            symbol=data.get("symbol", ""),
            amount=data.get("amount", "0"),
            address_from=data.get("address_from", ""),
            address_to=data.get("address_to", ""),
            txid=data.get("txid", ""),
            status=data.get("status", 0),
            confirm_count=data.get("confirm_count", 0),
            created_at=data.get("created_at", 0)
        )


@dataclass
class CoinInfo:
    """
    Cryptocurrency information.
    
    Attributes:
        symbol: Coin symbol
        base_symbol: Base chain symbol
        name: Coin name
        decimals: Decimal places
        contract_address: Smart contract address (for tokens)
        is_token: Whether this is a token
    """
    symbol: str
    base_symbol: str = ""
    name: str = ""
    decimals: int = 8
    contract_address: str = ""
    is_token: bool = False
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CoinInfo":
        """Create CoinInfo from dictionary."""
        return cls(
            symbol=data.get("symbol", ""),
            base_symbol=data.get("base_symbol", ""),
            name=data.get("name", ""),
            decimals=data.get("decimals", 8),
            contract_address=data.get("contract_address", ""),
            is_token=data.get("is_token", False)
        )


@dataclass
class UserInfo:
    """
    User information.
    
    Attributes:
        uid: User ID
        email: User email
        mobile: User mobile number
        country: Country code
    """
    uid: int
    email: str = ""
    mobile: str = ""
    country: str = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserInfo":
        """Create UserInfo from dictionary."""
        return cls(
            uid=data.get("uid", 0),
            email=data.get("email", ""),
            mobile=data.get("mobile", ""),
            country=data.get("country", "")
        )


@dataclass
class NotifyData:
    """
    Notification data from webhook callback.
    
    Attributes:
        side: Transaction side (deposit/withdraw)
        sub_wallet_id: Sub-wallet ID
        symbol: Cryptocurrency symbol
        amount: Transaction amount
        address_from: Source address
        address_to: Destination address
        txid: Blockchain transaction hash
        request_id: Merchant request ID
        status: Transaction status
    """
    side: str
    sub_wallet_id: int
    symbol: str
    amount: str
    address_from: str = ""
    address_to: str = ""
    txid: str = ""
    request_id: str = ""
    status: int = 0
    
    @property
    def transaction_side(self) -> TransactionSide:
        """Get transaction side as enum."""
        try:
            return TransactionSide(self.side)
        except ValueError:
            return TransactionSide.DEPOSIT
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NotifyData":
        """Create NotifyData from dictionary."""
        return cls(
            side=data.get("side", ""),
            sub_wallet_id=data.get("sub_wallet_id", 0),
            symbol=data.get("symbol", ""),
            amount=data.get("amount", "0"),
            address_from=data.get("address_from", ""),
            address_to=data.get("address_to", ""),
            txid=data.get("txid", ""),
            request_id=data.get("request_id", ""),
            status=data.get("status", 0)
        )


@dataclass
class AssetBalance:
    """
    Asset balance information.
    
    Attributes:
        symbol: Cryptocurrency symbol
        balance: Available balance
        frozen: Frozen balance
    """
    symbol: str
    balance: str = "0"
    frozen: str = "0"
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AssetBalance":
        """Create AssetBalance from dictionary."""
        return cls(
            symbol=data.get("symbol", ""),
            balance=data.get("balance", "0"),
            frozen=data.get("frozen", "0")
        )
