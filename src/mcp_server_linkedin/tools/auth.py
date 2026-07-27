"""Authentication tools — OAuth 2.0 flow, profile retrieval, logout.

Design principles:
- Tools are thin: validate input, delegate to services, format output.
- Each function receives dependencies explicitly (no global state).
- All exceptions are caught at the tool boundary and returned as strings.
"""

import logging
import secrets
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from urllib.parse import parse_qs, urlencode, urlparse

import httpx

from ..config import (
    LINKEDIN_AUTH_URL,
    LINKEDIN_TOKEN_URL,
    LinkedInSettings,
)
from ..exceptions import AuthenticationError, ConfigurationError, LinkedInAPIError
from ..services.linkedin import LinkedInService
from ..utils.token import delete_token, get_access_token, load_token, save_token

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Internal OAuth callback handler
# ---------------------------------------------------------------------------


class _OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Minimal HTTP handler that captures the OAuth redirect callback."""

    auth_code: str | None = None
    state: str | None = None
    error: str | None = None

    def do_GET(self) -> None:  # noqa: N802
        """Handle the GET request from LinkedIn's OAuth redirect."""
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if "error" in params:
            _OAuthCallbackHandler.error = params["error"][0]
            self._send_html("Authentication failed. You can close this window.")
        elif "code" in params:
            _OAuthCallbackHandler.auth_code = params["code"][0]
            _OAuthCallbackHandler.state = params.get("state", [None])[0]
            self._send_html("Authentication successful! You can close this window.")
        else:
            self._send_html("No authorization code received.")

    def _send_html(self, message: str) -> None:
        """Send a simple HTML page back to the user's browser."""
        html = (
            "<!DOCTYPE html><html><head><title>LinkedIn MCP Auth</title></head>"
            '<body style="font-family:system-ui;text-align:center;padding:60px">'
            f"<h2>{message}</h2>"
            "<p style='color:#666'>You can close this tab now.</p>"
            "</body></html>"
        )
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode())

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        """Suppress default HTTP server request logging."""


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _extract_port(redirect_uri: str) -> int:
    """Extract the port number from a redirect URI, defaulting to 3000."""
    parsed = urlparse(redirect_uri)
    return parsed.port or 3000


# ---------------------------------------------------------------------------
# MCP Tool implementations
# ---------------------------------------------------------------------------


async def linkedin_auth() -> str:
    """Authenticate with LinkedIn via OAuth 2.0.

    Opens the user's browser for authorization, starts a local HTTP server
    to capture the callback, exchanges the code for a token, and persists it.

    Returns:
        Success message with the authenticated user's name, or an error description.
    """
    # Load config
    try:
        settings = LinkedInSettings.from_env()
    except ConfigurationError as exc:
        return str(exc)

    # Check if already authenticated with a valid token
    existing_token = get_access_token()
    if existing_token:
        try:
            async with LinkedInService(existing_token) as svc:
                profile = await svc.get_profile()
            return (
                f"Already authenticated as {profile.name}. "
                "Use linkedin_logout to re-authenticate."
            )
        except LinkedInAPIError:
            pass  # Token expired — proceed with re-auth

    # Generate CSRF state
    state = secrets.token_urlsafe(32)
    port = _extract_port(settings.redirect_uri)

    # Build authorization URL
    auth_params = urlencode({
        "response_type": "code",
        "client_id": settings.client_id,
        "redirect_uri": settings.redirect_uri,
        "state": state,
        "scope": " ".join(settings.scopes),
    })
    auth_url = f"{LINKEDIN_AUTH_URL}?{auth_params}"

    # Reset handler state
    _OAuthCallbackHandler.auth_code = None
    _OAuthCallbackHandler.state = None
    _OAuthCallbackHandler.error = None

    # Start local callback server
    server = HTTPServer(("localhost", port), _OAuthCallbackHandler)
    server_thread = Thread(target=server.handle_request, daemon=True)
    server_thread.start()

    # Open browser for user consent
    webbrowser.open(auth_url)

    # Wait for the callback (timeout: 120s)
    server_thread.join(timeout=120)
    server.server_close()

    # Handle callback result
    if _OAuthCallbackHandler.error:
        return f"Authentication failed: {_OAuthCallbackHandler.error}"

    if not _OAuthCallbackHandler.auth_code:
        return "Authentication timed out. Please try again."

    if _OAuthCallbackHandler.state != state:
        return "Authentication failed: state mismatch (possible CSRF attack)."

    # Exchange authorization code for access token
    try:
        async with httpx.AsyncClient() as http:
            resp = await http.post(
                LINKEDIN_TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "code": _OAuthCallbackHandler.auth_code,
                    "redirect_uri": settings.redirect_uri,
                    "client_id": settings.client_id,
                    "client_secret": settings.client_secret,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

        if resp.status_code != 200:
            return f"Token exchange failed (HTTP {resp.status_code}): {resp.text}"

        token_data = resp.json()
        save_token(token_data)

        # Verify token by fetching profile
        async with LinkedInService(token_data["access_token"]) as svc:
            profile = await svc.get_profile()

        expires_days = token_data.get("expires_in", 0) // 86400
        return (
            f"Successfully authenticated as {profile.name}. "
            f"Token expires in {expires_days} days."
        )

    except Exception as exc:
        logger.exception("Token exchange error")
        return f"Authentication error: {exc}"


async def linkedin_get_profile() -> str:
    """Get the authenticated LinkedIn user's profile information.

    Returns:
        Formatted profile string, or an error message.
    """
    token = get_access_token()
    if not token:
        return str(AuthenticationError())

    try:
        async with LinkedInService(token) as svc:
            profile = await svc.get_profile()
        return profile.format_display()
    except LinkedInAPIError as exc:
        return f"Failed to fetch profile: {exc}"
    except Exception as exc:
        logger.exception("Unexpected error fetching profile")
        return f"Error: {exc}"


async def linkedin_logout() -> str:
    """Remove the stored LinkedIn authentication token.

    Returns:
        Confirmation that the token was deleted.
    """
    if delete_token():
        return "Logged out successfully. Token deleted."
    return "No token found — already logged out."
