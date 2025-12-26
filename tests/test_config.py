"""
Unit tests for config classes
"""
import pytest
from chainup_custody_sdk.waas.waas_config import WaasConfig
from chainup_custody_sdk.mpc.mpc_config import MpcConfig
from chainup_custody_sdk.exceptions import ConfigError


class TestWaasConfig:
    """Tests for WaasConfig."""
    
    def test_valid_config(self):
        """Test valid configuration."""
        config = WaasConfig(
            app_id="test-app",
            private_key="test-private-key",
            public_key="test-public-key"
        )
        assert config.validate() is True
        assert config.app_id == "test-app"
    
    def test_missing_app_id(self):
        """Test missing app_id raises ConfigError."""
        config = WaasConfig(
            app_id="",
            private_key="key",
            public_key="key"
        )
        with pytest.raises(ConfigError) as exc_info:
            config.validate()
        assert "app_id" in str(exc_info.value)
    
    def test_missing_private_key(self):
        """Test missing private_key raises ConfigError."""
        config = WaasConfig(
            app_id="test-app",
            private_key="",
            public_key="key"
        )
        with pytest.raises(ConfigError) as exc_info:
            config.validate()
        assert "private_key" in str(exc_info.value)
    
    def test_get_url(self):
        """Test URL generation."""
        config = WaasConfig(
            app_id="test",
            private_key="key",
            public_key="key"
        )
        url = config.get_url("/user/info")
        assert url == "https://openapi.chainup.com/v2/user/info"
    
    def test_host_normalization(self):
        """Test host URL is normalized with trailing slash."""
        config = WaasConfig(
            app_id="test",
            private_key="key",
            public_key="key",
            host="https://api.test.com"
        )
        assert config.host.endswith("/")
    
    def test_from_dict(self):
        """Test creating config from dictionary."""
        data = {
            "app_id": "test-app",
            "private_key": "private",
            "public_key": "public",
            "debug": True
        }
        config = WaasConfig.from_dict(data)
        assert config.app_id == "test-app"
        assert config.debug is True


class TestMpcConfig:
    """Tests for MpcConfig."""
    
    def test_valid_config(self):
        """Test valid MPC configuration."""
        config = MpcConfig(
            app_id="test-app",
            rsa_private_key="test-private-key"
        )
        assert config.validate() is True
    
    def test_missing_app_id(self):
        """Test missing app_id raises ConfigError."""
        config = MpcConfig(
            app_id="",
            rsa_private_key="key"
        )
        with pytest.raises(ConfigError) as exc_info:
            config.validate()
        assert "app_id" in str(exc_info.value)
    
    def test_missing_rsa_key(self):
        """Test missing rsa_private_key raises ConfigError."""
        config = MpcConfig(
            app_id="test-app",
            rsa_private_key=""
        )
        with pytest.raises(ConfigError) as exc_info:
            config.validate()
        assert "rsa_private_key" in str(exc_info.value)
    
    def test_get_url(self):
        """Test URL generation."""
        config = MpcConfig(
            app_id="test",
            rsa_private_key="key"
        )
        url = config.get_url("/api/mpc/wallet/create")
        assert url == "https://openapi.chainup.com/api/mpc/wallet/create"
    
    def test_from_dict(self):
        """Test creating config from dictionary."""
        data = {
            "app_id": "test-app",
            "rsa_private_key": "private",
            "waas_public_key": "public",
            "sign_private_key": "sign-key"
        }
        config = MpcConfig.from_dict(data)
        assert config.app_id == "test-app"
        assert config.sign_private_key == "sign-key"
