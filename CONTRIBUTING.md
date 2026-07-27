# Contributing to LinkedIn MCP Server

Thank you for your interest in contributing! This guide covers everything you need to get started.

## Development Setup

1. **Clone the repository:**

```bash
git clone https://github.com/Huzaifa-ali/mcp-server-linkedin.git
cd mcp-server-linkedin
```

2. **Install dependencies (requires [uv](https://docs.astral.sh/uv/)):**

```bash
uv sync --all-extras
```

3. **Set up pre-commit hooks:**

```bash
pre-commit install
```

4. **Copy the environment file and add your credentials:**

```bash
cp .env.example .env
```

## Project Structure

```
src/mcp_server_linkedin/
├── __init__.py          # Package metadata
├── config.py            # Constants, API URLs, LinkedInSettings dataclass
├── exceptions.py        # Typed exception hierarchy
├── server.py            # FastMCP entrypoint + direct tool registration
├── models/
│   └── linkedin.py      # Frozen dataclass models (LinkedInProfile, PostResult, etc.)
├── services/
│   └── linkedin.py      # Async API client with connection pooling
├── tools/
│   ├── auth.py          # OAuth flow, profile, logout
│   ├── posting.py       # Text, image, video, article, delete
│   └── analytics.py     # Stubbed (pending Community Management API)
└── utils/
    └── token.py         # Token file I/O (save, load, delete)
```

### Dependency Flow

```
tools/ → services/ → models/
tools/ → utils/
tools/ → config.py
services/ → config.py + exceptions.py + models/
```

Tools **never** import `httpx` directly. The service layer owns all HTTP communication.

## Making Changes

1. **Create a feature branch:**

```bash
git checkout -b feat/your-feature-name
```

2. **Follow code conventions:**
   - Type hints on all functions (use `X | None`, not `Optional[X]`)
   - Google-style docstrings on all public functions
   - Constants in `config.py`, never magic strings
   - Line length: 88 characters (enforced by Ruff)
   - Tools must never crash — catch exceptions at the boundary

3. **Run quality checks:**

```bash
uv run ruff check src/ tests/      # Lint
uv run ruff format src/ tests/     # Format
uv run mypy src/                   # Type check
uv run pytest                      # Test
```

Or run everything at once:

```bash
pre-commit run --all-files
```

4. **Commit with conventional commits:**

```bash
git commit -m "feat(posting): add support for carousel posts"
```

## Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix | Use |
|--------|-----|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation only |
| `refactor:` | Code restructuring (no behavior change) |
| `test:` | Adding/fixing tests |
| `chore:` | Build system, CI, tooling |
| `perf:` | Performance improvement |

Optional scopes: `auth`, `posting`, `analytics`, `server`, `config`, `docs`

## Adding a New Tool

1. Add the implementation in the appropriate `tools/` module
2. Keep it thin: **validate → delegate to service → format output string**
3. If it calls a new API endpoint, add the method to `services/linkedin.py`
4. If it returns new data, create a model in `models/linkedin.py`
5. Export from `tools/__init__.py`
6. Register in `server.py` with `mcp.tool()(your_function)`
7. Add a test in `tests/`
8. Document in `README.md` tool table

## Adding a New API Method

1. Add the method to `services/linkedin.py`
2. Use `self._client` (shared httpx client) for requests
3. Call `self._raise_for_status(resp, "description")` for error handling
4. Return a typed model, not a raw dict
5. Add a unit test mocking the HTTP response

## Pull Request Process

1. Ensure CI passes (lint + type check + tests)
2. Update `CHANGELOG.md` under `[Unreleased]`
3. Write a clear PR description explaining **what** and **why**
4. Link related issues with `Closes #123`
5. Keep PRs focused — one feature or fix per PR

## Running the Server Locally

```bash
uv run mcp-server-linkedin
```

Test with MCP Inspector:

```bash
npx @modelcontextprotocol/inspector uv run mcp-server-linkedin
```

## Reporting Issues

- Use [GitHub Issues](https://github.com/Huzaifa-ali/mcp-server-linkedin/issues)
- Include: Python version, OS, MCP client (Claude Desktop, Cursor, etc.)
- Include the full error message and steps to reproduce

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).
