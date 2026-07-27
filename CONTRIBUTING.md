# Contributing to mcp-server-linkedin

Thank you for your interest in contributing! This guide will help you get started.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/huzaifamalik47/mcp-server-linkedin.git
cd mcp-server-linkedin
```

2. Install dependencies with uv:
```bash
uv sync
```

3. Copy the environment file:
```bash
cp .env.example .env
```

4. Fill in your LinkedIn OAuth credentials in `.env`.

## Project Structure

```
src/mcp_server_linkedin/
├── __init__.py           # Package metadata
├── server.py             # MCP server entrypoint
├── config.py             # Configuration and constants
├── linkedin_client.py    # LinkedIn API client
└── tools/
    ├── __init__.py       # Tool exports
    ├── auth.py           # Authentication tools
    ├── posting.py        # Content publishing tools
    └── analytics.py      # Analytics tools (stubbed)
```

## Making Changes

1. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes following the code style:
   - Type hints on all functions
   - Google-style docstrings
   - Proper error handling (tools should never crash the server)
   - Use constants from `config.py`, not magic strings

3. Test your changes:
```bash
uv run mcp-server-linkedin
```

4. Commit with a clear message:
```bash
git commit -m "feat: add support for carousel posts"
```

## Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` — New feature
- `fix:` — Bug fix
- `docs:` — Documentation only
- `refactor:` — Code refactoring
- `chore:` — Build/tooling changes

## Pull Request Process

1. Update `CHANGELOG.md` with your changes under `[Unreleased]`
2. Ensure your code follows the existing patterns
3. Write a clear PR description explaining what and why
4. Link any related issues

## Adding New Tools

1. Create or modify a file in `src/mcp_server_linkedin/tools/`
2. Register the tool in `server.py` using the `@mcp.tool()` decorator
3. Follow the existing tool pattern:
   - Return descriptive strings (success with IDs, or error with context)
   - Handle all exceptions gracefully
   - Include proper type hints and docstrings
4. Document the tool in `README.md`

## Reporting Issues

- Use GitHub Issues
- Include your Python version, OS, and client (Claude Desktop, Cursor, etc.)
- Include the full error message and steps to reproduce

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).
