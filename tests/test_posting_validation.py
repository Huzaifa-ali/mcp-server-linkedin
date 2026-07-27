"""Tests for posting tool validation helpers."""

import pytest

from mcp_server_linkedin.tools.posting import (
    _require_text,
    _validate_visibility,
)


class TestValidateVisibility:
    """Tests for the _validate_visibility helper."""

    def test_public_uppercase(self) -> None:
        assert _validate_visibility("PUBLIC") == "PUBLIC"

    def test_connections_uppercase(self) -> None:
        assert _validate_visibility("CONNECTIONS") == "CONNECTIONS"

    def test_case_insensitive(self) -> None:
        assert _validate_visibility("public") == "PUBLIC"
        assert _validate_visibility("connections") == "CONNECTIONS"
        assert _validate_visibility("Public") == "PUBLIC"

    def test_strips_whitespace(self) -> None:
        assert _validate_visibility("  PUBLIC  ") == "PUBLIC"

    def test_invalid_raises(self) -> None:
        with pytest.raises(ValueError, match="Invalid visibility"):
            _validate_visibility("PRIVATE")

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="Invalid visibility"):
            _validate_visibility("")


class TestRequireText:
    """Tests for the _require_text helper."""

    def test_normal_text(self) -> None:
        assert _require_text("Hello world") == "Hello world"

    def test_strips_whitespace(self) -> None:
        assert _require_text("  spaced  ") == "spaced"

    def test_empty_string_raises(self) -> None:
        with pytest.raises(ValueError, match="cannot be empty"):
            _require_text("")

    def test_whitespace_only_raises(self) -> None:
        with pytest.raises(ValueError, match="cannot be empty"):
            _require_text("   \n\t  ")

    def test_none_like_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="cannot be empty"):
            _require_text("")
