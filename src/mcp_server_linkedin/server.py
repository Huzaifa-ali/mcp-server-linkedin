"""MCP server entrypoint — tool registration and lifecycle management.

Design principles:
- This file is a THIN orchestration layer. No business logic lives here.
- Tools are registered directly — no redundant wrapper functions.
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
# Tool registration — direct binding, no wrapper layer
# ---------------------------------------------------------------------------

# Authentication
mcp.tool()(linkedin_auth)
mcp.tool()(linkedin_get_profile)
mcp.tool()(linkedin_logout)

# Posting
mcp.tool()(linkedin_post_text)
mcp.tool()(linkedin_post_image)
mcp.tool()(linkedin_post_video)
mcp.tool()(linkedin_post_article)
mcp.tool()(linkedin_delete_post)

# Analytics
mcp.tool()(linkedin_get_post_stats)
mcp.tool()(linkedin_get_all_stats)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Run the LinkedIn MCP server."""
    logger.info("Starting mcp-server-linkedin...")
    mcp.run()


if __name__ == "__main__":
    main()
