"""MCP server entrypoint — tool registration and lifecycle management.

Design principles:
- This file is a THIN orchestration layer. No business logic lives here.
- Tools are registered directly — no redundant wrapper functions.
- Tool descriptions are written for LLM consumption: clear, specific, actionable.
- Logging is configured once at startup.
"""

import logging

from mcp.server.fastmcp import FastMCP

from .tools.analytics import linkedin_get_all_stats, linkedin_get_post_stats
from .tools.auth import linkedin_auth, linkedin_get_profile, linkedin_logout
from .tools.posting import (
    linkedin_delete_post,
    linkedin_post_article,
    linkedin_post_image,
    linkedin_post_text,
    linkedin_post_video,
)

# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# MCP server instance
# ---------------------------------------------------------------------------

mcp = FastMCP("mcp-server-linkedin")

# ---------------------------------------------------------------------------
# Tool registration with LLM-optimized descriptions
#
# Each description tells the LLM:
# 1. WHAT the tool does (action)
# 2. WHEN to use it (trigger condition)
# 3. WHAT it needs (key inputs)
# ---------------------------------------------------------------------------

# Authentication
mcp.tool(
    description=(
        "Authenticate with LinkedIn using OAuth 2.0. Opens a browser window for "
        "the user to log in and authorize. Must be called BEFORE any other LinkedIn "
        "tool if the user is not yet authenticated. Only needs to be run once — "
        "the token is saved and lasts 2 months."
    )
)(linkedin_auth)

mcp.tool(
    description=(
        "Get the currently authenticated LinkedIn user's profile: name, email, "
        "person URN, and profile picture URL. Use this to confirm who is logged in "
        "or to retrieve the user's identity. Requires prior authentication."
    )
)(linkedin_get_profile)

mcp.tool(
    description=(
        "Log out of LinkedIn by deleting the stored OAuth token. Use when the user "
        "wants to switch accounts or revoke access. After logout, linkedin_auth "
        "must be called again before using any other tools."
    )
)(linkedin_logout)

# Posting
mcp.tool(
    description=(
        "Publish a text-only post to LinkedIn. Use when the user wants to share a "
        "written update, thought, or announcement WITHOUT any image, video, or link "
        "preview. Requires: text content. Optional: visibility (PUBLIC or CONNECTIONS)."
    )
)(linkedin_post_text)

mcp.tool(
    description=(
        "Publish a LinkedIn post with an attached image. Use when the user wants to "
        "share a photo, infographic, screenshot, or any image file alongside text. "
        "Requires: text caption AND absolute file path to an image (JPEG, PNG, or GIF). "
        "Optional: visibility (PUBLIC or CONNECTIONS)."
    )
)(linkedin_post_image)

mcp.tool(
    description=(
        "Publish a LinkedIn post with an attached video. Use when the user wants to "
        "share a video file (MP4, max 200 MB) alongside text. Requires: text caption "
        "AND absolute file path to a video file. Optional: visibility (PUBLIC or CONNECTIONS)."
    )
)(linkedin_post_video)

mcp.tool(
    description=(
        "Publish a LinkedIn post with a link/article preview card. Use when the user "
        "wants to share a URL with an auto-generated preview (title, description, "
        "thumbnail). Best for sharing blog posts, news articles, or web pages. "
        "Requires: text commentary AND a URL. Optional: custom title, description, "
        "visibility (PUBLIC or CONNECTIONS)."
    )
)(linkedin_post_article)

mcp.tool(
    description=(
        "Delete an existing LinkedIn post. Use when the user wants to remove a post "
        "they previously published. Requires: the post URN/ID (e.g., "
        "urn:li:ugcPost:123456 or urn:li:share:123456). This action is irreversible."
    )
)(linkedin_delete_post)

# Analytics
mcp.tool(
    description=(
        "Get analytics (impressions, clicks, likes, comments, shares) for a specific "
        "LinkedIn post. NOTE: Currently requires Community Management API access "
        "(r_member_postAnalytics scope) which must be applied for separately at "
        "developer.linkedin.com. Returns instructions on how to gain access if not available."
    )
)(linkedin_get_post_stats)

mcp.tool(
    description=(
        "Get aggregated analytics across ALL LinkedIn posts (total impressions, clicks, "
        "likes, comments, shares). NOTE: Currently requires Community Management API "
        "access (r_member_postAnalytics scope) which must be applied for separately. "
        "Returns instructions on how to gain access if not available."
    )
)(linkedin_get_all_stats)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Run the LinkedIn MCP server."""
    logger.info("Starting mcp-server-linkedin...")
    mcp.run()


if __name__ == "__main__":
    main()
