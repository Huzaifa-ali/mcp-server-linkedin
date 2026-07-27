"""Analytics tools — stubbed pending Community Management API access.

These tools exist as placeholders so the MCP server advertises analytics
capability. Once LinkedIn grants Community Management API access
(r_member_postAnalytics scope), the implementations will call real endpoints.
"""

import logging

logger = logging.getLogger(__name__)

_COMMUNITY_MANAGEMENT_MSG = (
    "This feature requires the Community Management API "
    "(r_member_postAnalytics scope).\n\n"
    "To gain access:\n"
    "1. Apply at https://developer.linkedin.com/ for Community Management API\n"
    "2. Once approved, the r_member_postAnalytics scope will be available\n"
    "3. Re-authenticate with linkedin_auth to include the new scope\n\n"
    "Available metrics once enabled: impressions, clicks, likes, comments, "
    "shares, engagement rate, unique impressions."
)


async def linkedin_get_post_stats(
    post_id: str,
    metric: str = "impressions",
    aggregation: str = "daily",
    start_date: str = "",
    end_date: str = "",
) -> str:
    """Get analytics for a specific LinkedIn post.

    Note: Requires Community Management API access.

    Args:
        post_id: The post URN (e.g., urn:li:ugcPost:123456).
        metric: Metric to retrieve — impressions, clicks, likes, comments,
            shares, engagement.
        aggregation: Time aggregation — daily, weekly, monthly.
        start_date: Start date (YYYY-MM-DD). Defaults to 30 days ago.
        end_date: End date (YYYY-MM-DD). Defaults to today.

    Returns:
        Message explaining that Community Management API is required.
    """
    return f"Analytics for post {post_id} are not yet available.\n\n{_COMMUNITY_MANAGEMENT_MSG}"


async def linkedin_get_all_stats(
    metric: str = "impressions",
    aggregation: str = "daily",
    start_date: str = "",
    end_date: str = "",
) -> str:
    """Get aggregated analytics across all LinkedIn posts.

    Note: Requires Community Management API access.

    Args:
        metric: Metric to retrieve — impressions, clicks, likes, comments,
            shares, engagement.
        aggregation: Time aggregation — daily, weekly, monthly.
        start_date: Start date (YYYY-MM-DD). Defaults to 30 days ago.
        end_date: End date (YYYY-MM-DD). Defaults to today.

    Returns:
        Message explaining that Community Management API is required.
    """
    return f"Aggregated analytics are not yet available.\n\n{_COMMUNITY_MANAGEMENT_MSG}"
