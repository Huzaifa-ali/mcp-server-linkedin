"""Content publishing tools — text, image, video, article posts.

Design principles:
- Thin tool functions: validate → delegate → format.
- Shared validation helpers at module level (DRY).
- Each tool catches all exceptions at the boundary and returns a string.
- No direct httpx usage — all API calls go through LinkedInService.
"""

import logging

from ..config import VALID_VISIBILITIES, VISIBILITY_PUBLIC
from ..exceptions import (
    AuthenticationError,
    LinkedInAPIError,
    LinkedInMCPError,
    MediaUploadError,
)
from ..services.linkedin import LinkedInService
from ..utils.token import get_access_token

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Shared validation helpers
# ---------------------------------------------------------------------------


def _require_auth() -> str:
    """Return the access token or raise AuthenticationError."""
    token = get_access_token()
    if not token:
        raise AuthenticationError()
    return token


def _validate_visibility(visibility: str) -> str:
    """Normalize and validate the visibility parameter.

    Args:
        visibility: Raw visibility string from user input.

    Returns:
        Normalized uppercase visibility string.

    Raises:
        ValueError: If the visibility value is not recognized.
    """
    normalized = visibility.upper().strip()
    if normalized not in VALID_VISIBILITIES:
        raise ValueError(
            f"Invalid visibility '{visibility}'. Use PUBLIC or CONNECTIONS."
        )
    return normalized


def _require_text(text: str) -> str:
    """Validate that post text is non-empty.

    Returns:
        Stripped text.

    Raises:
        ValueError: If text is empty or whitespace-only.
    """
    stripped = text.strip() if text else ""
    if not stripped:
        raise ValueError("Post text cannot be empty.")
    return stripped


# ---------------------------------------------------------------------------
# MCP Tool implementations
# ---------------------------------------------------------------------------


async def linkedin_post_text(text: str, visibility: str = "PUBLIC") -> str:
    """Publish a text-only post to LinkedIn.

    Args:
        text: Post content (up to ~3000 characters recommended).
        visibility: "PUBLIC" or "CONNECTIONS".

    Returns:
        Success message with post ID, or error description.
    """
    try:
        clean_text = _require_text(text)
        vis = _validate_visibility(visibility)
        token = _require_auth()

        async with LinkedInService(token) as svc:
            profile = await svc.get_profile()
            result = await svc.create_text_post(profile.person_urn, clean_text, vis)

        return (
            f"Post published successfully.\n"
            f"Post ID: {result.post_id}\n"
            f"Visibility: {vis}"
        )

    except (ValueError, AuthenticationError) as exc:
        return f"Error: {exc}"
    except LinkedInAPIError as exc:
        return f"LinkedIn API error: {exc}"
    except Exception as exc:
        logger.exception("Unexpected error creating text post")
        return f"Error publishing post: {exc}"


async def linkedin_post_image(
    text: str, image_path: str, visibility: str = "PUBLIC"
) -> str:
    """Publish a post with an image to LinkedIn.

    Args:
        text: Post caption text.
        image_path: Absolute path to the image file (JPEG, PNG, GIF).
        visibility: "PUBLIC" or "CONNECTIONS".

    Returns:
        Success message with post ID, or error description.
    """
    try:
        clean_text = _require_text(text)
        vis = _validate_visibility(visibility)
        token = _require_auth()

        if not image_path or not image_path.strip():
            raise ValueError("image_path is required.")

        async with LinkedInService(token) as svc:
            profile = await svc.get_profile()
            author_urn = profile.person_urn

            # Register → Upload → Post
            upload_info = await svc.register_upload(author_urn, media_type="image")
            await svc.upload_media(upload_info.upload_url, image_path.strip())
            result = await svc.create_media_post(
                author_urn, clean_text, upload_info.asset_urn,
                media_type="image", visibility=vis,
            )

        return (
            f"Image post published successfully.\n"
            f"Post ID: {result.post_id}\n"
            f"Image: {image_path}\n"
            f"Visibility: {vis}"
        )

    except (ValueError, AuthenticationError, MediaUploadError) as exc:
        return f"Error: {exc}"
    except LinkedInAPIError as exc:
        return f"LinkedIn API error: {exc}"
    except Exception as exc:
        logger.exception("Unexpected error creating image post")
        return f"Error publishing image post: {exc}"


async def linkedin_post_video(
    text: str, video_path: str, visibility: str = "PUBLIC"
) -> str:
    """Publish a post with a video to LinkedIn.

    Args:
        text: Post caption text.
        video_path: Absolute path to the video file (MP4, max 200 MB).
        visibility: "PUBLIC" or "CONNECTIONS".

    Returns:
        Success message with post ID, or error description.
    """
    try:
        clean_text = _require_text(text)
        vis = _validate_visibility(visibility)
        token = _require_auth()

        if not video_path or not video_path.strip():
            raise ValueError("video_path is required.")

        async with LinkedInService(token) as svc:
            profile = await svc.get_profile()
            author_urn = profile.person_urn

            # Register → Upload → Post
            upload_info = await svc.register_upload(author_urn, media_type="video")
            await svc.upload_media(upload_info.upload_url, video_path.strip())
            result = await svc.create_media_post(
                author_urn, clean_text, upload_info.asset_urn,
                media_type="video", visibility=vis,
            )

        return (
            f"Video post published successfully.\n"
            f"Post ID: {result.post_id}\n"
            f"Video: {video_path}\n"
            f"Visibility: {vis}"
        )

    except (ValueError, AuthenticationError, MediaUploadError) as exc:
        return f"Error: {exc}"
    except LinkedInAPIError as exc:
        return f"LinkedIn API error: {exc}"
    except Exception as exc:
        logger.exception("Unexpected error creating video post")
        return f"Error publishing video post: {exc}"


async def linkedin_post_article(
    text: str,
    url: str,
    title: str = "",
    description: str = "",
    visibility: str = "PUBLIC",
) -> str:
    """Publish a post with a link/article preview to LinkedIn.

    Args:
        text: Post commentary text.
        url: Article URL (generates a link preview card).
        title: Optional title for the link preview.
        description: Optional description for the link preview.
        visibility: "PUBLIC" or "CONNECTIONS".

    Returns:
        Success message with post ID, or error description.
    """
    try:
        clean_text = _require_text(text)
        vis = _validate_visibility(visibility)
        token = _require_auth()

        if not url or not url.strip():
            raise ValueError("URL is required for article posts.")

        async with LinkedInService(token) as svc:
            profile = await svc.get_profile()
            result = await svc.create_article_post(
                profile.person_urn,
                clean_text,
                url.strip(),
                title=title,
                description=description,
                visibility=vis,
            )

        return (
            f"Article post published successfully.\n"
            f"Post ID: {result.post_id}\n"
            f"URL: {url}\n"
            f"Visibility: {vis}"
        )

    except (ValueError, AuthenticationError) as exc:
        return f"Error: {exc}"
    except LinkedInAPIError as exc:
        return f"LinkedIn API error: {exc}"
    except Exception as exc:
        logger.exception("Unexpected error creating article post")
        return f"Error publishing article post: {exc}"


async def linkedin_delete_post(post_id: str) -> str:
    """Delete a LinkedIn post by its URN.

    Args:
        post_id: Post URN (e.g., urn:li:ugcPost:123456 or urn:li:share:123456).

    Returns:
        Success confirmation or error message.
    """
    try:
        if not post_id or not post_id.strip():
            raise ValueError("post_id is required.")

        token = _require_auth()

        async with LinkedInService(token) as svc:
            await svc.delete_post(post_id.strip())

        return f"Post deleted successfully.\nPost ID: {post_id}"

    except (ValueError, AuthenticationError) as exc:
        return f"Error: {exc}"
    except LinkedInAPIError as exc:
        return f"LinkedIn API error: {exc}"
    except Exception as exc:
        logger.exception("Unexpected error deleting post")
        return f"Error deleting post: {exc}"
