"""Pydantic models for LinkedIn API responses.

Design principles:
- Each model maps to a distinct API response shape.
- ``from_api_response()`` class methods handle the raw dict → model conversion.
- Models are immutable (frozen) to prevent accidental mutation.
- Keep models thin — no business logic, only data + validation.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LinkedInProfile:
    """User profile returned by the /v2/userinfo endpoint."""

    sub: str
    name: str
    email: str
    picture: str | None = None

    @property
    def person_urn(self) -> str:
        """Construct the LinkedIn Person URN from the subject identifier."""
        return f"urn:li:person:{self.sub}"

    @classmethod
    def from_api_response(cls, data: dict[str, object]) -> LinkedInProfile:
        """Parse a raw userinfo API response into a LinkedInProfile.

        Args:
            data: JSON response dict from /v2/userinfo.

        Returns:
            A validated LinkedInProfile instance.
        """
        return cls(
            sub=str(data.get("sub", "")),
            name=str(data.get("name", "Unknown")),
            email=str(data.get("email", "")),
            picture=str(data["picture"]) if data.get("picture") else None,
        )

    def format_display(self) -> str:
        """Format profile for human-readable tool output."""
        lines = [
            f"Name: {self.name}",
            f"Email: {self.email}",
            f"Person URN: {self.person_urn}",
        ]
        if self.picture:
            lines.append(f"Picture: {self.picture}")
        return "\n".join(lines)


@dataclass(frozen=True, slots=True)
class MediaUploadInfo:
    """Parsed response from the register-upload endpoint."""

    upload_url: str
    asset_urn: str

    @classmethod
    def from_api_response(cls, data: dict[str, object]) -> MediaUploadInfo:
        """Extract upload URL and asset URN from the register-upload response.

        Args:
            data: JSON response dict from /v2/assets?action=registerUpload.

        Returns:
            A MediaUploadInfo with the upload endpoint and asset identifier.

        Raises:
            KeyError: If the response structure is unexpected.
        """
        value = data["value"]  # type: ignore[index]
        upload_mechanism = value["uploadMechanism"]  # type: ignore[index]
        http_request = upload_mechanism[
            "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
        ]
        upload_url = str(http_request["uploadUrl"])  # type: ignore[index]
        asset_urn = str(value["asset"])  # type: ignore[index]

        return cls(upload_url=upload_url, asset_urn=asset_urn)


@dataclass(frozen=True, slots=True)
class PostResult:
    """Successful post creation result."""

    post_id: str
    post_urn: str | None = None

    @classmethod
    def from_api_response(cls, data: dict[str, object]) -> PostResult:
        """Parse a UGC post creation response.

        Args:
            data: JSON response dict from /v2/ugcPosts.

        Returns:
            A PostResult with the post identifier.
        """
        post_id = str(data.get("id", "unknown"))
        return cls(post_id=post_id, post_urn=post_id)
