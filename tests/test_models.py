"""
Unit tests for models module
"""
import pytest
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


class TestApiResponse:
    """Tests for ApiResponse model."""
    
    def test_success_response(self):
        """Test successful API response."""
        response = ApiResponse(code=0, msg="success", data={"id": 123})
        assert response.is_success is True
        assert response.code == 0
        assert response.data == {"id": 123}
    
    def test_error_response(self):
        """Test error API response."""
        response = ApiResponse(code=1001, msg="Invalid parameter")
        assert response.is_success is False
        assert response.code == 1001
    
    def test_from_dict(self):
        """Test creating from dictionary."""
        data = {"code": 0, "msg": "success", "data": {"test": True}}
        response = ApiResponse.from_dict(data)
        assert response.code == 0
        assert response.data == {"test": True}


class TestWalletInfo:
    """Tests for WalletInfo model."""
    
    def test_wallet_info(self):
        """Test wallet info creation."""
        wallet = WalletInfo(
            sub_wallet_id=1000,
            sub_wallet_name="Test Wallet",
            symbol="ETH",
            address="0x123"
        )
        assert wallet.sub_wallet_id == 1000
        assert wallet.sub_wallet_name == "Test Wallet"
    
    def test_from_dict(self):
        """Test creating from dictionary."""
        data = {"sub_wallet_id": 1000, "sub_wallet_name": "Test"}
        wallet = WalletInfo.from_dict(data)
        assert wallet.sub_wallet_id == 1000


class TestTransactionRecord:
    """Tests for TransactionRecord model."""
    
    def test_transaction_record(self):
        """Test transaction record."""
        record = TransactionRecord(
            id=1,
            request_id="req-123",
            symbol="ETH",
            amount="1.5",
            status=2
        )
        assert record.transaction_status == TransactionStatus.SUCCESS
    
    def test_unknown_status(self):
        """Test unknown transaction status."""
        record = TransactionRecord(
            id=1,
            request_id="req-123",
            symbol="ETH",
            amount="1.5",
            status=999
        )
        assert record.transaction_status == TransactionStatus.PENDING


class TestNotifyData:
    """Tests for NotifyData model."""
    
    def test_deposit_notification(self):
        """Test deposit notification."""
        notify = NotifyData(
            side="deposit",
            sub_wallet_id=1000,
            symbol="ETH",
            amount="1.0"
        )
        assert notify.transaction_side == TransactionSide.DEPOSIT
    
    def test_withdraw_notification(self):
        """Test withdraw notification."""
        notify = NotifyData(
            side="withdraw",
            sub_wallet_id=1000,
            symbol="BTC",
            amount="0.5"
        )
        assert notify.transaction_side == TransactionSide.WITHDRAW
    
    def test_from_dict(self):
        """Test creating from dictionary."""
        data = {
            "side": "deposit",
            "sub_wallet_id": 1000,
            "symbol": "ETH",
            "amount": "1.0",
            "txid": "0xabc123"
        }
        notify = NotifyData.from_dict(data)
        assert notify.txid == "0xabc123"


class TestAssetBalance:
    """Tests for AssetBalance model."""
    
    def test_asset_balance(self):
        """Test asset balance."""
        balance = AssetBalance(symbol="ETH", balance="10.5", frozen="0.5")
        assert balance.symbol == "ETH"
        assert balance.balance == "10.5"
        assert balance.frozen == "0.5"
    
    def test_default_values(self):
        """Test default values."""
        balance = AssetBalance(symbol="BTC")
        assert balance.balance == "0"
        assert balance.frozen == "0"
