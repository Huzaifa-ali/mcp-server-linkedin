"""Configuration constants and settings for the LinkedIn MCP server.

Single responsibility: defines API URLs, limits, and the settings dataclass.
No file I/O — token management lives in utils/token.py.
"""

import os
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# LinkedIn API endpoints
# ---------------------------------------------------------------------------

LINKEDIN_AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
LINKEDIN_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
LINKEDIN_API_BASE = "https://api.linkedin.com/v2"
LINKEDIN_USERINFO_URL = "https://api.linkedin.com/v2/userinfo"
LINKEDIN_UGC_POSTS_URL = "https://api.linkedin.com/v2/ugcPosts"
LINKEDIN_REGISTER_UPLOAD_URL = "https://api.linkedin.com/v2/assets?action=registerUpload"

# ---------------------------------------------------------------------------
# OAuth scopes
# ---------------------------------------------------------------------------

OAUTH_SCOPES: list[str] = ["openid", "profile", "email", "w_member_social"]

# ---------------------------------------------------------------------------
# Protocol headers
# ---------------------------------------------------------------------------

RESTLI_HEADER: dict[str, str] = {"X-Restli-Protocol-Version": "2.0.0"}

# ---------------------------------------------------------------------------
# Media upload recipes
# ---------------------------------------------------------------------------

IMAGE_RECIPE = "urn:li:digitalmediaRecipe:feedshare-image"
VIDEO_RECIPE = "urn:li:digitalmediaRecipe:feedshare-video"

# ---------------------------------------------------------------------------
# Limits
# ---------------------------------------------------------------------------

RATE_LIMIT_REQUESTS_PER_DAY = 150
TOKEN_DURATION_SECONDS = 5_184_000  # ~2 months

MAX_VIDEO_SIZE_BYTES = 200 * 1024 * 1024  # 200 MB
MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB (LinkedIn limit)

# ---------------------------------------------------------------------------
# Visibility constants
# ---------------------------------------------------------------------------

VISIBILITY_PUBLIC = "PUBLIC"
VISIBILITY_CONNECTIONS = "CONNECTIONS"
VALID_VISIBILITIES = frozenset({VISIBILITY_PUBLIC, VISIBILITY_CONNECTIONS})

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

DEFAULT_REDIRECT_URI = "http://localhost:3000/callback"
DEFAULT_HTTP_TIMEOUT = 30.0
UPLOAD_HTTP_TIMEOUT = 300.0


# ---------------------------------------------------------------------------
# Settings dataclass — loaded from environment
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class LinkedInSettings:
    """Immutable, type-safe configuration loaded from environment variables.

    Use ``LinkedInSettings.from_env()`` to construct an instance.
    Raises ``ConfigurationError`` if required variables are missing.
    """

    client_id: str
    client_secret: str
    redirect_uri: str = DEFAULT_REDIRECT_URI
    scopes: list[str] = field(default_factory=lambda: list(OAUTH_SCOPES))

    @classmethod
    def from_env(cls) -> "LinkedInSettings":
        """Load settings from environment variables.

        Returns:
            A validated LinkedInSettings instance.

        Raises:
            ConfigurationError: If LINKEDIN_CLIENT_ID or LINKEDIN_CLIENT_SECRET
                are not set.
        """
        from .exceptions import ConfigurationError

        client_id = os.environ.get("LINKEDIN_CLIENT_ID", "")
        client_secret = os.environ.get("LINKEDIN_CLIENT_SECRET", "")
        redirect_uri = os.environ.get("LINKEDIN_REDIRECT_URI", DEFAULT_REDIRECT_URI)

        if not client_id or not client_secret:
            raise ConfigurationError(
                "LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET environment variables "
                "are required. Create a LinkedIn app at "
                "https://www.linkedin.com/developers/apps and set these values."
            )

        return cls(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
        )
