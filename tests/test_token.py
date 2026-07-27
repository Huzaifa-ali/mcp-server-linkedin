"""Tests for token persistence utilities."""

import json
from pathlib import Path

from mcp_server_linkedin.utils.token import (
    delete_token,
    get_access_token,
    load_token,
    save_token,
)


class TestTokenPersistence:
    """Tests for token save/load/delete operations."""

    def test_save_and_load(self, tmp_path: Path) -> None:
        token_file = tmp_path / "token.json"
        token_data = {"access_token": "abc123", "expires_in": 5184000}

        save_token(token_data, path=token_file)
        loaded = load_token(path=token_file)

        assert loaded is not None
        assert loaded["access_token"] == "abc123"
        assert loaded["expires_in"] == 5184000

    def test_load_nonexistent(self, tmp_path: Path) -> None:
        token_file = tmp_path / "does_not_exist.json"
        assert load_token(path=token_file) is None

    def test_load_invalid_json(self, tmp_path: Path) -> None:
        token_file = tmp_path / "bad.json"
        token_file.write_text("not json at all {{{", encoding="utf-8")
        assert load_token(path=token_file) is None

    def test_delete_existing(self, tmp_path: Path) -> None:
        token_file = tmp_path / "token.json"
        token_file.write_text("{}", encoding="utf-8")

        assert delete_token(path=token_file) is True
        assert not token_file.exists()

    def test_delete_nonexistent(self, tmp_path: Path) -> None:
        token_file = tmp_path / "nope.json"
        assert delete_token(path=token_file) is False

    def test_get_access_token(self, tmp_path: Path) -> None:
        token_file = tmp_path / "token.json"
        token_data = {"access_token": "my_token_value", "token_type": "bearer"}
        token_file.write_text(json.dumps(token_data), encoding="utf-8")

        result = get_access_token(path=token_file)
        assert result == "my_token_value"

    def test_get_access_token_no_file(self, tmp_path: Path) -> None:
        token_file = tmp_path / "missing.json"
        assert get_access_token(path=token_file) is None

    def test_save_creates_directory(self, tmp_path: Path) -> None:
        nested_path = tmp_path / "deep" / "nested" / "token.json"
        save_token({"access_token": "x"}, path=nested_path)
        assert nested_path.exists()
