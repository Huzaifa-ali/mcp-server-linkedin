"""Token persistence — load, save, and delete OAuth tokens from disk.

Single responsibility: this module ONLY handles token file I/O.
It knows nothing about LinkedIn, HTTP clients, or config resolution.
"""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Default token storage location
TOKEN_DIR: Path = Path.home() / ".mcp-server-linkedin"
TOKEN_FILE: Path = TOKEN_DIR / "token.json"


def save_token(token_data: dict[str, Any], *, path: Path = TOKEN_FILE) -> None:
    """Persist an OAuth token response to disk.

    Args:
        token_data: Token response dict from LinkedIn OAuth.
        path: File path to write. Defaults to ~/.mcp-server-linkedin/token.json.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(token_data, indent=2), encoding="utf-8")
    logger.info("Token saved to %s", path)


def load_token(*, path: Path = TOKEN_FILE) -> dict[str, Any] | None:
    """Read a saved OAuth token from disk.

    Args:
        path: File path to read. Defaults to ~/.mcp-server-linkedin/token.json.

    Returns:
        Token data dict if the file exists and is valid JSON, None otherwise.
    """
    if not path.exists():
        return None

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Failed to load token file: %s", exc)
        return None


def delete_token(*, path: Path = TOKEN_FILE) -> bool:
    """Remove the stored OAuth token file.

    Args:
        path: File path to delete. Defaults to ~/.mcp-server-linkedin/token.json.

    Returns:
        True if the file was deleted, False if it did not exist.
    """
    if path.exists():
        path.unlink()
        logger.info("Token deleted from %s", path)
        return True
    return False


def get_access_token(*, path: Path = TOKEN_FILE) -> str | None:
    """Convenience — extract the access_token string from the stored file.

    Args:
        path: File path to read. Defaults to ~/.mcp-server-linkedin/token.json.

    Returns:
        The access token string, or None if unavailable.
    """
    token_data = load_token(path=path)
    if token_data is None:
        return None
    return token_data.get("access_token")
