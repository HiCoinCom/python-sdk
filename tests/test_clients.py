"""
Unit tests for client classes
"""
import pytest
from unittest.mock import Mock, patch
from chainup_custody_sdk import WaasClient, MpcClient
from chainup_custody_sdk.waas.waas_config import WaasConfig
from chainup_custody_sdk.mpc.mpc_config import MpcConfig


class TestWaasClient:
    """Tests for WaasClient."""
    
    def test_builder_pattern(self):
        """Test builder pattern creates client correctly."""
        client = (
            WaasClient.builder()
            .set_app_id("test-app")
            .set_private_key("test-private-key")
            .set_public_key("test-public-key")
            .set_debug(True)
            .build()
        )
        assert client.config.app_id == "test-app"
        assert client.config.debug is True
    
    def test_new_builder_alias(self):
        """Test new_builder is alias for builder."""
        builder1 = WaasClient.builder()
        builder2 = WaasClient.new_builder()
        assert type(builder1) == type(builder2)
    
    def test_context_manager(self):
        """Test context manager support."""
        client = (
            WaasClient.builder()
            .set_app_id("test")
            .set_private_key("key")
            .set_public_key("key")
            .build()
        )
        
        with client as c:
            assert c._closed is False
        
        assert client._closed is True
    
    def test_get_api_instances(self):
        """Test API factory methods return correct types."""
        client = (
            WaasClient.builder()
            .set_app_id("test")
            .set_private_key("key")
            .set_public_key("key")
            .build()
        )
        
        from chainup_custody_sdk.waas.api.user_api import UserApi
        from chainup_custody_sdk.waas.api.account_api import AccountApi
        from chainup_custody_sdk.waas.api.billing_api import BillingApi
        
        assert isinstance(client.get_user_api(), UserApi)
        assert isinstance(client.get_account_api(), AccountApi)
        assert isinstance(client.get_billing_api(), BillingApi)


class TestMpcClient:
    """Tests for MpcClient."""
    
    def test_builder_pattern(self):
        """Test builder pattern creates client correctly."""
        client = (
            MpcClient.builder()
            .set_app_id("test-app")
            .set_rsa_private_key("test-private-key")
            .set_waas_public_key("test-public-key")
            .set_sign_private_key("sign-key")
            .set_debug(True)
            .build()
        )
        assert client.config.app_id == "test-app"
        assert client.config.sign_private_key == "sign-key"
        assert client.config.debug is True
    
    def test_context_manager(self):
        """Test context manager support."""
        client = (
            MpcClient.builder()
            .set_app_id("test")
            .set_rsa_private_key("key")
            .build()
        )
        
        with client as c:
            assert c._closed is False
        
        assert client._closed is True
    
    def test_get_api_instances(self):
        """Test API factory methods return correct types."""
        client = (
            MpcClient.builder()
            .set_app_id("test")
            .set_rsa_private_key("key")
            .build()
        )
        
        from chainup_custody_sdk.mpc.api.wallet_api import WalletApi
        from chainup_custody_sdk.mpc.api.deposit_api import DepositApi
        from chainup_custody_sdk.mpc.api.withdraw_api import WithdrawApi
        
        assert isinstance(client.get_wallet_api(), WalletApi)
        assert isinstance(client.get_deposit_api(), DepositApi)
        assert isinstance(client.get_withdraw_api(), WithdrawApi)


class TestClientBuilderChaining:
    """Tests for builder method chaining."""
    
    def test_waas_builder_returns_self(self):
        """Test WaaS builder methods return self for chaining."""
        builder = WaasClient.builder()
        
        assert builder.set_app_id("test") is builder
        assert builder.set_private_key("key") is builder
        assert builder.set_public_key("key") is builder
        assert builder.set_host("https://test.com") is builder
        assert builder.set_version("v3") is builder
        assert builder.set_charset("UTF-8") is builder
        assert builder.set_debug(True) is builder
    
    def test_mpc_builder_returns_self(self):
        """Test MPC builder methods return self for chaining."""
        builder = MpcClient.builder()
        
        assert builder.set_app_id("test") is builder
        assert builder.set_rsa_private_key("key") is builder
        assert builder.set_waas_public_key("key") is builder
        assert builder.set_sign_private_key("key") is builder
        assert builder.set_domain("https://test.com") is builder
        assert builder.set_api_key("key") is builder
        assert builder.set_debug(True) is builder
