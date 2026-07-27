<p align="center">
  <img src="assets/banner.png" alt="LinkedIn MCP Server — Plug AI into LinkedIn" width="100%" />
</p>

# LinkedIn MCP Server

[![PyPI](https://img.shields.io/pypi/v/mcp-server-linkedin.svg)](https://pypi.org/project/mcp-server-linkedin/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-compatible-purple.svg)](https://modelcontextprotocol.io)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

The LinkedIn MCP Server connects AI tools directly to LinkedIn's platform. Publish posts with text, images, videos, and article links — all through natural language from any MCP-compatible client.

### Use Cases

- **Content Publishing:** Draft and publish LinkedIn posts from your AI assistant without switching context.
- **Media Sharing:** Upload images and videos alongside your posts in a single command.
- **Link Previews:** Share articles with auto-generated link preview cards.
- **Multi-Format Workflow:** Compose text-only updates, visual content, or article shares through one unified interface.
- **Account Management:** Authenticate, check your profile, and manage your session without leaving your editor.

Built for developers and content creators who want their AI tools to publish directly to LinkedIn.

---

## Quick Start

### Prerequisites

1. **Python 3.10+**
2. **LinkedIn App** — Create one at [LinkedIn Developer Portal](https://www.linkedin.com/developers/apps)
   - Products: "Share on LinkedIn" + "Sign In with LinkedIn using OpenID Connect"
   - OAuth 2.0 scopes: `openid`, `profile`, `email`, `w_member_social`
   - Redirect URL: `http://localhost:3000/callback`

### Install

```bash
uvx mcp-server-linkedin
```

Or with pip:

```bash
pip install mcp-server-linkedin
```

---

## Configuration

Set these environment variables:

```bash
LINKEDIN_CLIENT_ID=your_client_id        # From LinkedIn Developer Portal
LINKEDIN_CLIENT_SECRET=your_secret_here  # From LinkedIn Developer Portal
LINKEDIN_REDIRECT_URI=http://localhost:3000/callback  # Optional, this is the default
```

### Claude Desktop

Add to your `claude_desktop_config.json`:

<details>
<summary>macOS: ~/Library/Application Support/Claude/claude_desktop_config.json</summary>

```json
{
  "mcpServers": {
    "linkedin": {
      "command": "uvx",
      "args": ["mcp-server-linkedin"],
      "env": {
        "LINKEDIN_CLIENT_ID": "your_client_id",
        "LINKEDIN_CLIENT_SECRET": "your_secret_here"
      }
    }
  }
}
```

</details>

<details>
<summary>Windows: %APPDATA%\Claude\claude_desktop_config.json</summary>

```json
{
  "mcpServers": {
    "linkedin": {
      "command": "uvx",
      "args": ["mcp-server-linkedin"],
      "env": {
        "LINKEDIN_CLIENT_ID": "your_client_id",
        "LINKEDIN_CLIENT_SECRET": "your_secret_here"
      }
    }
  }
}
```

</details>

### VS Code + Copilot

Add to `.vscode/mcp.json` in your workspace:

```json
{
  "servers": {
    "linkedin": {
      "command": "uvx",
      "args": ["mcp-server-linkedin"],
      "env": {
        "LINKEDIN_CLIENT_ID": "your_client_id",
        "LINKEDIN_CLIENT_SECRET": "your_secret_here"
      }
    }
  }
}
```

### Cursor

Add to `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "linkedin": {
      "command": "uvx",
      "args": ["mcp-server-linkedin"],
      "env": {
        "LINKEDIN_CLIENT_ID": "your_client_id",
        "LINKEDIN_CLIENT_SECRET": "your_secret_here"
      }
    }
  }
}
```

### Kiro

Add to `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "linkedin": {
      "command": "uvx",
      "args": ["mcp-server-linkedin"],
      "env": {
        "LINKEDIN_CLIENT_ID": "your_client_id",
        "LINKEDIN_CLIENT_SECRET": "your_secret_here"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add linkedin -- uvx mcp-server-linkedin
```

Then set `LINKEDIN_CLIENT_ID` and `LINKEDIN_CLIENT_SECRET` in your environment.

### Windsurf

Add to your Windsurf MCP configuration:

```json
{
  "mcpServers": {
    "linkedin": {
      "command": "uvx",
      "args": ["mcp-server-linkedin"],
      "env": {
        "LINKEDIN_CLIENT_ID": "your_client_id",
        "LINKEDIN_CLIENT_SECRET": "your_secret_here"
      }
    }
  }
}
```

### Running from Source

Replace `"command": "uvx", "args": ["mcp-server-linkedin"]` with:

```json
{
  "command": "uv",
  "args": ["--directory", "/path/to/mcp-server-linkedin", "run", "mcp-server-linkedin"]
}
```

---

## Authentication

1. Start your MCP client (Claude Desktop, Kiro, etc.)
2. Ask: *"Authenticate with LinkedIn"*
3. Browser opens → authorize the app → callback captured automatically
4. Token saved to `~/.mcp-server-linkedin/token.json`
5. Token lasts **2 months**. Re-run `linkedin_auth` when it expires.

---

## Tools

| Tool | Description |
|------|-------------|
| `linkedin_auth` | OAuth 2.0 browser-based authentication |
| `linkedin_get_profile` | Get your name, email, and person URN |
| `linkedin_logout` | Remove stored token |
| `linkedin_post_text` | Publish a text-only post |
| `linkedin_post_image` | Publish a post with an image |
| `linkedin_post_video` | Publish a post with a video (up to 200 MB) |
| `linkedin_post_article` | Publish a post with a link preview |
| `linkedin_delete_post` | Delete a post by ID |
| `linkedin_get_post_stats` | Get post analytics *(requires Community Management API)* |
| `linkedin_get_all_stats` | Get aggregated analytics *(requires Community Management API)* |

### Tool Details

<details>
<summary><b>linkedin_post_text</b></summary>

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | string | *required* | Post content (up to ~3000 chars) |
| `visibility` | string | `"PUBLIC"` | `"PUBLIC"` or `"CONNECTIONS"` |

</details>

<details>
<summary><b>linkedin_post_image</b></summary>

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | string | *required* | Post caption |
| `image_path` | string | *required* | Absolute path to image (JPEG, PNG, GIF) |
| `visibility` | string | `"PUBLIC"` | `"PUBLIC"` or `"CONNECTIONS"` |

</details>

<details>
<summary><b>linkedin_post_video</b></summary>

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | string | *required* | Post caption |
| `video_path` | string | *required* | Absolute path to video (MP4, max 200 MB) |
| `visibility` | string | `"PUBLIC"` | `"PUBLIC"` or `"CONNECTIONS"` |

</details>

<details>
<summary><b>linkedin_post_article</b></summary>

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | string | *required* | Post commentary |
| `url` | string | *required* | Article URL (generates link preview) |
| `title` | string | `""` | Optional link preview title |
| `description` | string | `""` | Optional link preview description |
| `visibility` | string | `"PUBLIC"` | `"PUBLIC"` or `"CONNECTIONS"` |

</details>

<details>
<summary><b>linkedin_delete_post</b></summary>

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `post_id` | string | *required* | Post URN (e.g., `urn:li:ugcPost:123456`) |

</details>

---

## Architecture

```
src/mcp_server_linkedin/
├── config.py            # Constants, API URLs, settings dataclass
├── exceptions.py        # Typed exception hierarchy
├── server.py            # FastMCP entrypoint + tool registration
├── models/              # Frozen dataclass API response models
├── services/            # Async API client with connection pooling
├── tools/               # MCP tool implementations (validate → delegate → format)
│   ├── auth.py          # OAuth flow, profile, logout
│   ├── posting.py       # Text, image, video, article, delete
│   └── analytics.py     # Stubbed (pending API access)
└── utils/               # Token persistence
```

---

## Rate Limits

| Limit | Value |
|-------|-------|
| API requests per member per day | 150 |
| Token duration | 2 months |
| Max video file size | 200 MB |

The server relays LinkedIn's rate limit errors clearly but does not enforce limits internally.

---

## Security

- **Tokens stored locally** at `~/.mcp-server-linkedin/token.json`
- **No credentials in code** — all secrets via environment variables
- **Official API only** — uses `w_member_social` scope
- **Local OAuth callback** — authorization code never leaves your machine
- **No data collection** — this server sends nothing except LinkedIn API calls

---

## Development

```bash
git clone https://github.com/Huzaifa-ali/mcp-server-linkedin.git
cd mcp-server-linkedin
uv sync --all-extras
pre-commit install
```

```bash
uv run mcp-server-linkedin                    # Run the server
uv run ruff check src/                        # Lint
uv run ruff format src/                       # Format
uv run mypy src/                              # Type check
uv run pytest                                 # Test
```

Test with MCP Inspector:

```bash
npx @modelcontextprotocol/inspector uv run mcp-server-linkedin
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. In short:

1. Fork the repo and create a feature branch
2. Make your changes with type hints and docstrings
3. Run `pre-commit run --all-files` (must pass)
4. Open a pull request

---

## License

MIT — see [LICENSE](LICENSE).
