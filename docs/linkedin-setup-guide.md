# LinkedIn MCP Server — Setup Guide

This guide walks you through the complete setup from creating a LinkedIn app to publishing your first post via an AI agent.

---

## Table of Contents

1. [Create a LinkedIn App](#1-create-a-linkedin-app)
2. [Request Required Products](#2-request-required-products)
3. [Configure OAuth Redirect URL](#3-configure-oauth-redirect-url)
4. [Get Your Client ID and Secret](#4-get-your-client-id-and-secret)
5. [Install the MCP Server](#5-install-the-mcp-server)
6. [Configure Your AI Client](#6-configure-your-ai-client)
7. [Authenticate](#7-authenticate)
8. [Publish Your First Post](#8-publish-your-first-post)
9. [Troubleshooting](#9-troubleshooting)

---

## 1. Create a LinkedIn App

1. Go to the [LinkedIn Developer Portal](https://www.linkedin.com/developers/apps)
2. Click **"Create app"**
3. Fill in the required fields:

| Field | What to enter |
|-------|---------------|
| **App name** | Any name (e.g., "My AI Publisher") |
| **LinkedIn Page** | Select your LinkedIn Company Page* |
| **Privacy policy URL** | Your website URL (can be your GitHub repo URL) |
| **App logo** | Upload any square image (100x100px minimum) |

4. Check the legal agreement box and click **"Create app"**

> *LinkedIn requires a Company Page. If you don't have one, [create a Company Page](https://www.linkedin.com/company/setup/new/) first (takes 30 seconds — you can use your name as the company name).

<!-- SCREENSHOT: LinkedIn Create App form filled out -->
<!-- Place screenshot at: docs/images/01-create-app.png -->

---

## 2. Request Required Products

After creating your app, you need to enable two products:

1. Go to your app → **Products** tab
2. Request access to these two products:

| Product | Why it's needed |
|---------|----------------|
| **Share on LinkedIn** | Allows posting text, images, videos, articles |
| **Sign In with LinkedIn using OpenID Connect** | Provides profile access + OAuth scopes |

3. Click **"Request access"** for each product
4. Accept the terms

> Both products should be approved **instantly** for most developers. If "Share on LinkedIn" shows as pending, wait a few minutes and refresh.

<!-- SCREENSHOT: Products tab showing both products enabled/requested -->
<!-- Place screenshot at: docs/images/02-products.png -->

After approval, your app will have these OAuth 2.0 scopes available:
- `openid` — OpenID Connect
- `profile` — Read basic profile
- `email` — Read email address
- `w_member_social` — Create, edit, delete posts

---

## 3. Configure OAuth Redirect URL

1. Go to your app → **Auth** tab
2. Scroll down to **"OAuth 2.0 settings"**
3. Under **"Authorized redirect URLs for your app"**, click the pencil/edit icon
4. Add this URL:

```
http://localhost:3000/callback
```

5. Click **"Update"** to save

> This is the URL where LinkedIn sends the authorization code after you log in. The MCP server starts a temporary local server on port 3000 to capture it.

<!-- SCREENSHOT: Auth tab showing redirect URL configured -->
<!-- Place screenshot at: docs/images/03-redirect-url.png -->

---

## 4. Get Your Client ID and Secret

1. Stay on the **Auth** tab
2. You'll see two values at the top:

| Field | Description |
|-------|-------------|
| **Client ID** | A public identifier for your app (e.g., `77abc123xyz`) |
| **Client Secret** | A private key — **never share this publicly** |

3. Click the eye icon to reveal the Client Secret, then copy both values

> Keep these safe. You'll need them in the next step.

<!-- SCREENSHOT: Auth tab showing Client ID and Client Secret fields (secret blurred) -->
<!-- Place screenshot at: docs/images/04-credentials.png -->

---

## 5. Install the MCP Server

Choose one method:

### Option A: Using uvx (recommended, no install needed)

```bash
uvx mcp-server-linkedin
```

This downloads and runs the server on the fly. No permanent installation.

### Option B: Using pip

```bash
pip install mcp-server-linkedin
```

### Option C: From source

```bash
git clone https://github.com/Huzaifa-ali/mcp-server-linkedin.git
cd mcp-server-linkedin
uv sync
```

---

## 6. Configure Your AI Client

Add the server configuration to your MCP client. Replace `your_client_id` and `your_secret_here` with the values from Step 4.

<details>
<summary><b>Claude Desktop</b></summary>

File location:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

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
<summary><b>VS Code + Copilot</b></summary>

File: `.vscode/mcp.json` in your workspace

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

</details>

<details>
<summary><b>Cursor</b></summary>

File: `.cursor/mcp.json` in your project root

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
<summary><b>Kiro</b></summary>

File: `.kiro/settings/mcp.json`

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
<summary><b>Claude Code (CLI)</b></summary>

```bash
claude mcp add linkedin -- uvx mcp-server-linkedin
```

Then set environment variables:

```bash
export LINKEDIN_CLIENT_ID="your_client_id"
export LINKEDIN_CLIENT_SECRET="your_secret_here"
```

</details>

<details>
<summary><b>Windsurf</b></summary>

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

</details>

---

## 7. Authenticate

1. Open your AI client (Claude Desktop, Cursor, etc.)
2. Ask the agent:

> "Authenticate with LinkedIn"

3. Your browser will open to LinkedIn's login/consent page:

<!-- SCREENSHOT: LinkedIn OAuth consent screen showing permissions -->
<!-- Place screenshot at: docs/images/05-oauth-consent.png -->

4. Click **"Allow"** to authorize
5. You'll see a success page in your browser:

<!-- SCREENSHOT: Browser showing "Authentication successful! You can close this window." -->
<!-- Place screenshot at: docs/images/06-auth-success.png -->

6. Back in your AI client, you'll see a confirmation:

```
Successfully authenticated as Jane Developer. Token expires in 59 days.
```

> The token is saved to `~/.mcp-server-linkedin/token.json` and lasts **2 months**. You won't need to authenticate again until it expires.

---

## 8. Publish Your First Post

Now try these commands in your AI client:

### Text post

> "Post to LinkedIn: Excited to announce that I've automated my LinkedIn publishing with AI! #MCP #Automation"

### Image post

> "Post this image to LinkedIn with caption 'Our new office view!' — file is at /Users/me/Desktop/office.jpg"

### Article share

> "Share this article on LinkedIn: https://example.com/my-blog-post with the caption 'Great read on AI automation'"

### Check your profile

> "Show me my LinkedIn profile"

---

## 9. Troubleshooting

### "LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET must be set"

Your environment variables aren't reaching the server. Double-check:
- The `env` section in your MCP config JSON
- No typos in the variable names
- The JSON file is valid (no trailing commas)

### "Authentication timed out"

The browser OAuth flow didn't complete within 120 seconds. Try again and make sure:
- Your browser opened the LinkedIn consent page
- You clicked "Allow"
- Port 3000 isn't blocked by another app (check with `lsof -i :3000` on Mac/Linux or `netstat -an | findstr 3000` on Windows)

### "Authentication failed: state mismatch"

This usually means you had a stale auth attempt. Try:
1. Run `linkedin_logout`
2. Run `linkedin_auth` again

### "Failed to fetch profile: (HTTP 401)"

Your token has expired. Run `linkedin_auth` again to get a fresh token.

### "Share on LinkedIn" product not showing

Some LinkedIn apps need to be associated with a verified Company Page. Make sure:
- Your Company Page exists and is published (not in draft)
- You are listed as an admin on that Company Page

### Port 3000 already in use

If another app is using port 3000, set a custom redirect URI:

1. In LinkedIn Developer Portal → Auth → change redirect URL to `http://localhost:8080/callback`
2. In your MCP config, add:

```json
"env": {
  "LINKEDIN_CLIENT_ID": "your_id",
  "LINKEDIN_CLIENT_SECRET": "your_secret",
  "LINKEDIN_REDIRECT_URI": "http://localhost:8080/callback"
}
```

---

## Next Steps

- Browse all available tools: see the [README tool reference](../README.md#tools)
- Report issues: [GitHub Issues](https://github.com/Huzaifa-ali/mcp-server-linkedin/issues)
- Contribute: [Contributing Guide](../CONTRIBUTING.md)
