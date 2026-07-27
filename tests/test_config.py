"""Tests for configuration module."""

import os
from unittest.mock import patch

import pytest

from mcp_server_linkedin.config import (
    DEFAULT_REDIRECT_URI,
    LINKEDIN_API_BASE,
    VALID_VISIBILITIES,
    VISIBILITY_CONNECTIONS,
    VISIBILITY_PUBLIC,
    LinkedInSettings,
)
from mcp_server_linkedin.exceptions import ConfigurationError


class TestConstants:
    """Test configuration constants are properly defined."""

    def test_api_base_url(self) -> None:
        assert LINKEDIN_API_BASE == "https://api.linkedin.com/v2"

    def test_visibility_options(self) -> None:
        assert VISIBILITY_PUBLIC == "PUBLIC"
        assert VISIBILITY_CONNECTIONS == "CONNECTIONS"
        assert VALID_VISIBILITIES == frozenset({"PUBLIC", "CONNECTIONS"})

    def test_default_redirect_uri(self) -> None:
        assert "localhost" in DEFAULT_REDIRECT_URI
        assert "3000" in DEFAULT_REDIRECT_URI


class TestLinkedInSettings:
    """Tests for LinkedInSettings dataclass."""

    def test_from_env_success(self) -> None:
        env = {
            "LINKEDIN_CLIENT_ID": "test_id",
            "LINKEDIN_CLIENT_SECRET": "test_secret",
            "LINKEDIN_REDIRECT_URI": "http://localhost:9000/cb",
        }
        with patch.dict(os.environ, env, clear=False):
            settings = LinkedInSettings.from_env()
        assert settings.client_id == "test_id"
        assert settings.client_secret == "test_secret"
        assert settings.redirect_uri == "http://localhost:9000/cb"

    def test_from_env_missing_client_id(self) -> None:
        env = {"LINKEDIN_CLIENT_SECRET": "secret"}
        with patch.dict(os.environ, env, clear=False):
            # Remove CLIENT_ID if it exists
            os.environ.pop("LINKEDIN_CLIENT_ID", None)
            with pytest.raises(ConfigurationError):
                LinkedInSettings.from_env()

    def test_from_env_missing_client_secret(self) -> None:
        env = {"LINKEDIN_CLIENT_ID": "id_val"}
        with patch.dict(os.environ, env, clear=False):
            os.environ.pop("LINKEDIN_CLIENT_SECRET", None)
            with pytest.raises(ConfigurationError):
                LinkedInSettings.from_env()

    def test_from_env_default_redirect_uri(self) -> None:
        env = {
            "LINKEDIN_CLIENT_ID": "id",
            "LINKEDIN_CLIENT_SECRET": "secret",
        }
        with patch.dict(os.environ, env, clear=False):
            os.environ.pop("LINKEDIN_REDIRECT_URI", None)
            settings = LinkedInSettings.from_env()
        assert settings.redirect_uri == DEFAULT_REDIRECT_URI

    def test_frozen_immutability(self) -> None:
        settings = LinkedInSettings(client_id="a", client_secret="b")
        with pytest.raises(AttributeError):
            settings.client_id = "changed"  # type: ignore[misc]
