"""Structured exception hierarchy for the LinkedIn MCP server.

Design principles:
- Each exception type maps to a distinct failure category.
- All exceptions carry enough context for actionable error messages.
- Tool-layer code catches these and formats user-facing strings.
"""


class LinkedInMCPError(Exception):
    """Base exception for all LinkedIn MCP server errors."""


class AuthenticationError(LinkedInMCPError):
    """Raised when the user is not authenticated or the token is invalid."""

    def __init__(self, message: str = "Not authenticated. Run linkedin_auth first."):
        super().__init__(message)


class ConfigurationError(LinkedInMCPError):
    """Raised when required configuration (env vars, settings) is missing."""

    def __init__(self, message: str):
        super().__init__(message)


class LinkedInAPIError(LinkedInMCPError):
    """Raised when a LinkedIn API call returns a non-success status.

    Attributes:
        status_code: HTTP status code from the API response.
        detail: Raw response body for debugging.
    """

    def __init__(
        self, message: str, *, status_code: int | None = None, detail: str = ""
    ):
        self.status_code = status_code
        self.detail = detail
        super().__init__(message)

    def __str__(self) -> str:
        parts = [super().__str__()]
        if self.status_code:
            parts.append(f"(HTTP {self.status_code})")
        if self.detail:
            parts.append(f"Detail: {self.detail}")
        return " ".join(parts)


class MediaUploadError(LinkedInMCPError):
    """Raised when media file validation or upload fails."""

    def __init__(self, message: str):
        super().__init__(message)


class ValidationError(LinkedInMCPError):
    """Raised when tool input validation fails (bad visibility, empty text, etc.)."""

    def __init__(self, message: str):
        super().__init__(message)
