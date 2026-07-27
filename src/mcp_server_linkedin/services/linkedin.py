"""Async LinkedIn API service with connection pooling.

Single responsibility: HTTP communication with LinkedIn's API.
- Uses a shared httpx.AsyncClient for connection reuse.
- Returns typed model objects, not raw dicts.
- Raises structured exceptions on failure.
- Knows nothing about MCP tools, tokens on disk, or user interaction.
"""

import logging
from pathlib import Path
from typing import Any

import httpx

from ..config import (
    DEFAULT_HTTP_TIMEOUT,
    IMAGE_RECIPE,
    LINKEDIN_API_BASE,
    LINKEDIN_REGISTER_UPLOAD_URL,
    LINKEDIN_UGC_POSTS_URL,
    LINKEDIN_USERINFO_URL,
    MAX_VIDEO_SIZE_BYTES,
    RESTLI_HEADER,
    UPLOAD_HTTP_TIMEOUT,
    VIDEO_RECIPE,
    VISIBILITY_PUBLIC,
)
from ..exceptions import LinkedInAPIError, MediaUploadError
from ..models.linkedin import LinkedInProfile, MediaUploadInfo, PostResult

logger = logging.getLogger(__name__)


class LinkedInService:
    """Async client wrapping LinkedIn API v2 endpoints.

    This class manages a persistent httpx.AsyncClient for efficient
    connection pooling. Use as an async context manager or call
    ``close()`` explicitly when done.

    Example:
        async with LinkedInService(access_token="...") as svc:
            profile = await svc.get_profile()
    """

    def __init__(self, access_token: str) -> None:
        """Initialize the service with an OAuth access token.

        Args:
            access_token: A valid LinkedIn OAuth 2.0 bearer token.
        """
        self._token = access_token
        self._client = httpx.AsyncClient(
            base_url=LINKEDIN_API_BASE,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                **RESTLI_HEADER,
            },
            timeout=DEFAULT_HTTP_TIMEOUT,
        )

    async def __aenter__(self) -> "LinkedInService":
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.close()

    async def close(self) -> None:
        """Close the underlying HTTP client and release connections."""
        await self._client.aclose()

    # ------------------------------------------------------------------
    # Profile
    # ------------------------------------------------------------------

    async def get_profile(self) -> LinkedInProfile:
        """Fetch the authenticated user's profile.

        Returns:
            A LinkedInProfile instance with sub, name, email, picture.

        Raises:
            LinkedInAPIError: If the API returns a non-200 status.
        """
        resp = await self._client.get(LINKEDIN_USERINFO_URL)
        self._raise_for_status(resp, "fetch profile")
        return LinkedInProfile.from_api_response(resp.json())

    # ------------------------------------------------------------------
    # Posts
    # ------------------------------------------------------------------

    async def create_text_post(
        self,
        author_urn: str,
        text: str,
        visibility: str = VISIBILITY_PUBLIC,
    ) -> PostResult:
        """Publish a text-only post.

        Args:
            author_urn: Person URN (e.g., urn:li:person:abc123).
            text: Post body text.
            visibility: PUBLIC or CONNECTIONS.

        Returns:
            PostResult with the new post ID.

        Raises:
            LinkedInAPIError: On API failure.
        """
        payload = self._build_post_payload(
            author_urn=author_urn,
            text=text,
            visibility=visibility,
            media_category="NONE",
        )

        resp = await self._client.post(LINKEDIN_UGC_POSTS_URL, json=payload)
        self._raise_for_status(resp, "create text post")
        return PostResult.from_api_response(resp.json())

    async def create_media_post(
        self,
        author_urn: str,
        text: str,
        asset_urn: str,
        *,
        media_type: str = "image",
        title: str = "",
        visibility: str = VISIBILITY_PUBLIC,
    ) -> PostResult:
        """Publish a post with an image or video attachment.

        Args:
            author_urn: Person URN.
            text: Post body text.
            asset_urn: Asset URN from a completed upload registration.
            media_type: Either "image" or "video".
            title: Optional media title.
            visibility: PUBLIC or CONNECTIONS.

        Returns:
            PostResult with the new post ID.

        Raises:
            LinkedInAPIError: On API failure.
        """
        media_category = "IMAGE" if media_type == "image" else "VIDEO"

        media_entry: dict[str, Any] = {"status": "READY", "media": asset_urn}
        if title:
            media_entry["title"] = {"text": title}

        payload = self._build_post_payload(
            author_urn=author_urn,
            text=text,
            visibility=visibility,
            media_category=media_category,
            media=[media_entry],
        )

        resp = await self._client.post(LINKEDIN_UGC_POSTS_URL, json=payload)
        self._raise_for_status(resp, "create media post")
        return PostResult.from_api_response(resp.json())

    async def create_article_post(
        self,
        author_urn: str,
        text: str,
        url: str,
        *,
        title: str = "",
        description: str = "",
        visibility: str = VISIBILITY_PUBLIC,
    ) -> PostResult:
        """Publish a post with a link/article preview.

        Args:
            author_urn: Person URN.
            text: Post commentary text.
            url: Article URL.
            title: Optional link preview title.
            description: Optional link preview description.
            visibility: PUBLIC or CONNECTIONS.

        Returns:
            PostResult with the new post ID.

        Raises:
            LinkedInAPIError: On API failure.
        """
        media_entry: dict[str, Any] = {"status": "READY", "originalUrl": url}
        if title:
            media_entry["title"] = {"text": title}
        if description:
            media_entry["description"] = {"text": description}

        payload = self._build_post_payload(
            author_urn=author_urn,
            text=text,
            visibility=visibility,
            media_category="ARTICLE",
            media=[media_entry],
        )

        resp = await self._client.post(LINKEDIN_UGC_POSTS_URL, json=payload)
        self._raise_for_status(resp, "create article post")
        return PostResult.from_api_response(resp.json())

    async def delete_post(self, post_urn: str) -> None:
        """Delete a post by its URN.

        Args:
            post_urn: Full post URN (e.g., urn:li:ugcPost:123456).

        Raises:
            LinkedInAPIError: If deletion fails.
        """
        url = f"/ugcPosts/{post_urn}"
        resp = await self._client.delete(url)
        self._raise_for_status(resp, "delete post", expected=(200, 204))

    # ------------------------------------------------------------------
    # Media upload
    # ------------------------------------------------------------------

    async def register_upload(
        self, author_urn: str, *, media_type: str = "image"
    ) -> MediaUploadInfo:
        """Register a media upload slot with LinkedIn.

        Args:
            author_urn: Person URN.
            media_type: "image" or "video".

        Returns:
            MediaUploadInfo with upload_url and asset_urn.

        Raises:
            LinkedInAPIError: If registration fails.
        """
        recipe = IMAGE_RECIPE if media_type == "image" else VIDEO_RECIPE

        payload = {
            "registerUploadRequest": {
                "recipes": [recipe],
                "owner": author_urn,
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent",
                    }
                ],
            }
        }

        resp = await self._client.post(LINKEDIN_REGISTER_UPLOAD_URL, json=payload)
        self._raise_for_status(resp, "register upload")
        return MediaUploadInfo.from_api_response(resp.json())

    async def upload_media(self, upload_url: str, file_path: str) -> None:
        """Upload a media file to the registered upload URL.

        Args:
            upload_url: URL returned from register_upload.
            file_path: Local path to the media file.

        Raises:
            MediaUploadError: If the file is missing or too large.
            LinkedInAPIError: If the upload HTTP request fails.
        """
        path = Path(file_path)
        if not path.exists():
            raise MediaUploadError(f"File not found: {file_path}")

        file_size = path.stat().st_size
        if file_size > MAX_VIDEO_SIZE_BYTES:
            raise MediaUploadError(
                f"File size ({file_size / 1024 / 1024:.1f} MB) exceeds "
                f"maximum allowed ({MAX_VIDEO_SIZE_BYTES / 1024 / 1024:.0f} MB)."
            )

        upload_headers = {
            "Authorization": f"Bearer {self._token}",
            **RESTLI_HEADER,
        }

        # Use a separate client with extended timeout for uploads
        async with httpx.AsyncClient(timeout=UPLOAD_HTTP_TIMEOUT) as upload_client:
            with open(path, "rb") as f:
                resp = await upload_client.put(
                    upload_url,
                    headers=upload_headers,
                    content=f.read(),
                )

        if resp.status_code not in (200, 201):
            raise LinkedInAPIError(
                "Failed to upload media",
                status_code=resp.status_code,
                detail=resp.text,
            )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_post_payload(
        *,
        author_urn: str,
        text: str,
        visibility: str,
        media_category: str,
        media: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Construct the UGC post payload.

        Centralizes payload building to avoid repetition across post methods.
        """
        share_content: dict[str, Any] = {
            "shareCommentary": {"text": text},
            "shareMediaCategory": media_category,
        }
        if media:
            share_content["media"] = media

        return {
            "author": author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {"com.linkedin.ugc.ShareContent": share_content},
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": visibility},
        }

    @staticmethod
    def _raise_for_status(
        resp: httpx.Response,
        action: str,
        expected: tuple[int, ...] = (200, 201),
    ) -> None:
        """Raise LinkedInAPIError if the response status is unexpected.

        Args:
            resp: The httpx Response object.
            action: Human-readable description of what was attempted.
            expected: Tuple of acceptable HTTP status codes.
        """
        if resp.status_code not in expected:
            raise LinkedInAPIError(
                f"Failed to {action}",
                status_code=resp.status_code,
                detail=resp.text,
            )
