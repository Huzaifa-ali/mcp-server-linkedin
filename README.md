# mcp-server-linkedin

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-compatible-purple.svg)](https://modelcontextprotocol.io)

An MCP server that lets AI agents publish content to LinkedIn using the official API. Works with any MCP-compatible client — Claude Desktop, Kiro, Cursor, VS Code + Copilot, Claude Code, Windsurf, and more.

## Features

| Tool | Description |
|------|-------------|
| `linkedin_auth` | OAuth 2.0 browser-based authentication |
| `linkedin_get_profile` | Get your name, email, and person URN |
| `linkedin_logout` | Remove stored token |
| `linkedin_post_text` | Publish a text-only post |
| `linkedin_post_image` | Publish a post with an image |
| `linkedin_post_video` | Publish a post with a video (up to 200MB) |
| `linkedin_post_article` | Publish a post with a link preview |
| `linkedin_delete_post` | Delete a post by ID |
| `linkedin_get_post_stats` | Get post analytics *(requires Community Management API)* |
| `linkedin_get_all_stats` | Get aggregated analytics *(requires Community Management API)* |

## Prerequisites

1. **Python 3.10+**
2. **LinkedIn App** — Create one at [LinkedIn Developer Portal](https://www.linkedin.com/developers/apps)
   - Products: "Share on LinkedIn" and "Sign In with LinkedIn using OpenID Connect"
   - OAuth 2.0 scopes: `openid`, `profile`, `email`, `w_member_social`
   - Redirect URL: `http://localhost:3000/callback`

## Installation

### Using uvx (recommended)

```bash
uvx mcp-server-linkedin
```

### Using pip

```bash
pip install mcp-server-linkedin
```

### From source

```bash
git clone https://github.com/huzaifamalik47/mcp-server-linkedin.git
cd mcp-server-linkedin
uv sync
```

## Configuration

Set these environment variables (or use a `.env` file with your client):

```bash
LINKEDIN_CLIENT_ID=77hiy6ir3rz91y        # Your LinkedIn app client ID
LINKEDIN_CLIENT_SECRET=your_secret_here    # Your LinkedIn app client secret
LINKEDIN_REDIRECT_URI=http://localhost:3000/callback
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
        "LINKEDIN_CLIENT_ID": "77hiy6ir3rz91y",
        "LINKEDIN_CLIENT_SECRET": "your_secret_here",
        "LINKEDIN_REDIRECT_URI": "http://localhost:3000/callback"
      }
    }
  }
}
```

### Claude Desktop

Add to `claude_desktop_config.json`:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "linkedin": {
      "command": "uvx",
      "args": ["mcp-server-linkedin"],
      "env": {
        "LINKEDIN_CLIENT_ID": "77hiy6ir3rz91y",
        "LINKEDIN_CLIENT_SECRET": "your_secret_here",
        "LINKEDIN_REDIRECT_URI": "http://localhost:3000/callback"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add linkedin -- uvx mcp-server-linkedin
```

Then set environment variables in your shell or `.env` file.

### Cursor

Add to `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "linkedin": {
      "command": "uvx",
      "args": ["mcp-server-linkedin"],
      "env": {
        "LINKEDIN_CLIENT_ID": "77hiy6ir3rz91y",
        "LINKEDIN_CLIENT_SECRET": "your_secret_here",
        "LINKEDIN_REDIRECT_URI": "http://localhost:3000/callback"
      }
    }
  }
}
```

### VS Code + Copilot

Add to `.vscode/mcp.json` in your workspace:

```json
{
  "servers": {
    "linkedin": {
      "command": "uvx",
      "args": ["mcp-server-linkedin"],
      "env": {
        "LINKEDIN_CLIENT_ID": "77hiy6ir3rz91y",
        "LINKEDIN_CLIENT_SECRET": "your_secret_here",
        "LINKEDIN_REDIRECT_URI": "http://localhost:3000/callback"
      }
    }
  }
}
```

### Windsurf

Add to your Windsurf MCP configuration:

```json
{
  "mcpServers": {
    "linkedin": {
      "command": "uvx",
      "args": ["mcp-server-linkedin"],
      "env": {
        "LINKEDIN_CLIENT_ID": "77hiy6ir3rz91y",
        "LINKEDIN_CLIENT_SECRET": "your_secret_here",
        "LINKEDIN_REDIRECT_URI": "http://localhost:3000/callback"
      }
    }
  }
}
```

### Running from source (any client)

Replace `"command": "uvx", "args": ["mcp-server-linkedin"]` with:

```json
{
  "command": "uv",
  "args": ["--directory", "/path/to/mcp-server-linkedin", "run", "mcp-server-linkedin"]
}
```

## First-Run Authentication

1. Start your MCP client (Claude Desktop, Kiro, etc.)
2. Ask the agent: *"Authenticate with LinkedIn"*
3. The agent calls `linkedin_auth` → your browser opens LinkedIn's consent page
4. Authorize the app → browser redirects to `localhost:3000/callback`
5. Token is saved to `~/.mcp-server-linkedin/token.json`
6. Done. Token lasts 2 months. Re-run `linkedin_auth` when it expires.

## Tool Reference

### linkedin_auth

Authenticates via OAuth 2.0. Opens browser, captures callback, saves token.

### linkedin_get_profile

Returns your LinkedIn profile: name, email, person URN, profile picture.

### linkedin_logout

Deletes the stored token file. Requires re-authentication afterward.

### linkedin_post_text

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | string | *required* | Post content (up to ~3000 chars) |
| `visibility` | string | `"PUBLIC"` | `"PUBLIC"` or `"CONNECTIONS"` |

### linkedin_post_image

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | string | *required* | Post caption |
| `image_path` | string | *required* | Absolute path to image (JPEG, PNG, GIF) |
| `visibility` | string | `"PUBLIC"` | `"PUBLIC"` or `"CONNECTIONS"` |

### linkedin_post_video

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | string | *required* | Post caption |
| `video_path` | string | *required* | Absolute path to video (MP4, max 200MB) |
| `visibility` | string | `"PUBLIC"` | `"PUBLIC"` or `"CONNECTIONS"` |

### linkedin_post_article

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | string | *required* | Post commentary |
| `url` | string | *required* | Article URL (generates link preview) |
| `title` | string | `""` | Optional link preview title |
| `description` | string | `""` | Optional link preview description |
| `visibility` | string | `"PUBLIC"` | `"PUBLIC"` or `"CONNECTIONS"` |

### linkedin_delete_post

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `post_id` | string | *required* | Post URN (e.g., `urn:li:ugcPost:123456`) |

### linkedin_get_post_stats / linkedin_get_all_stats

Currently stubbed — returns a message explaining Community Management API is required.

## Rate Limits

| Limit | Value |
|-------|-------|
| API requests per member per day | 150 |
| Token duration | 2 months (5,184,000 seconds) |
| Max video file size | 200 MB |

The server does not enforce rate limits internally but will relay LinkedIn's rate limit errors clearly.

## Security

- **Tokens stored locally** at `~/.mcp-server-linkedin/token.json` (user-only permissions)
- **No credentials in code** — all secrets via environment variables
- **Official API only** — `w_member_social` scope, zero ban risk
- **Local OAuth callback** — authorization code never leaves your machine
- **No data collection** — this server sends nothing except LinkedIn API calls

## Development

```bash
git clone https://github.com/huzaifamalik47/mcp-server-linkedin.git
cd mcp-server-linkedin
uv sync
uv run mcp-server-linkedin
```

Test with MCP Inspector:
```bash
npx @modelcontextprotocol/inspector uv run mcp-server-linkedin
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT — see [LICENSE](LICENSE).
