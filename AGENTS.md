# AGENTS.md — AI Development Guidelines

> **Audience:** LLM-driven engineering agents

---

## Repository Map

| Path | Purpose |
| --- | --- |
| `src/mcp_server_linkedin/` | Library source (Python ≥ 3.10) |
| `  ├─ config.py` | Constants, API URLs, `LinkedInSettings` dataclass |
| `  ├─ exceptions.py` | Typed exception hierarchy (`LinkedInAPIError`, etc.) |
| `  ├─ server.py` | FastMCP instance + direct tool registration (entrypoint) |
| `  ├─ models/` | Frozen dataclass models (`LinkedInProfile`, `PostResult`, etc.) |
| `  ├─ services/` | Async API clients with connection pooling (`LinkedInService`) |
| `  ├─ tools/` | MCP tool implementations (thin: validate → delegate → format) |
| `  │   ├─ auth.py` | OAuth flow, profile, logout |
| `  │   ├─ posting.py` | Text, image, video, article posts + delete |
| `  │   └─ analytics.py` | Stubbed — pending Community Management API |
| `  └─ utils/` | Shared utilities (token persistence) |
| `tests/` | Pytest suite (unit + integration) |

---

## Architecture

- **Single Responsibility:** Each module does one thing. Config has no I/O. Token module has no API knowledge. Service has no MCP awareness.
- **Dependency flow:** `tools/ → services/ → models/` + `tools/ → utils/` + `tools/ → config.py`
- **No wrapper pattern:** Tools are registered directly with `mcp.tool()` — no pass-through functions.
- **Connection pooling:** `LinkedInService` wraps a persistent `httpx.AsyncClient` with proper lifecycle.
- **Typed models:** API responses are parsed into frozen dataclasses with `from_api_response()` factory methods.
- **Structured exceptions:** Typed exception hierarchy caught at tool boundary, never leaks to MCP layer.
- **Tool naming:** `linkedin_{action}_{target}` (e.g., `linkedin_post_text`, `linkedin_get_profile`).

---

## Key Principles

1. **Never crash the server.** Every tool catches exceptions and returns a descriptive error string.
2. **Type hints everywhere.** All functions, parameters, and return values.
3. **Google-style docstrings.** On every public function.
4. **Constants over magic strings.** All API URLs, headers, and values live in `config.py`.
5. **Tools return strings.** Success messages include relevant IDs; errors include context.
6. **Single responsibility per file.** If a module does two things, split it.

---

## Code Style

- Python 3.10+ — use `X | None` not `Optional[X]`
- Use `async/await` for all API interactions
- Import from relative modules (`from ..config import ...`)
- No star imports
- Logging via `logging.getLogger(__name__)`
- Line length: 88 characters (Ruff enforced)
- Formatting: Ruff (replaces Black)
- Linting: Ruff (replaces Flake8 + isort)
- Type checking: mypy (strict mode)

---

## Adding a New Tool

1. Add the implementation function in the appropriate `tools/` module
2. Keep it thin: validate input → call service → format output string
3. Export it from `tools/__init__.py`
4. Register it in `server.py` with `mcp.tool()(your_function)`
5. Update `README.md` tool reference table

## Adding a New API Method

1. Add the method to `services/linkedin.py`
2. If it returns new data, create a model in `models/linkedin.py`
3. Add appropriate exception handling using `_raise_for_status()`
4. The tool layer calls the service; it never touches httpx directly

---

## Dev Workflow

```bash
uv sync --frozen --all-extras        # install all dependencies
pre-commit install                    # setup git hooks
pre-commit run --all-files           # Ruff + mypy
uv run pytest -xvs                   # full test suite
uv run pytest --cov                  # with coverage
uv run ruff check src/               # lint only
uv run ruff format src/              # format only
uv run mypy src/                     # type check only
```

*Lint/typing must be clean before committing.*

---

## Rules

1. **Package management:** ONLY use `uv`, NEVER `pip`
2. **Type safety:** All functions require full type annotations
3. **Testing:** New features need tests, bug fixes need regression tests
4. **Commit types:** `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
5. **No wrapper functions:** Register tools directly, no pass-through layers
6. **Service layer owns HTTP:** Tools never import httpx directly

---

## LinkedIn API Notes

- API v2 with UGC Posts endpoint
- Always include `X-Restli-Protocol-Version: 2.0.0` header
- Media uploads: register → upload binary → create post with asset URN
- Person URN format: `urn:li:person:{sub}` (from userinfo endpoint)
- Rate limit: 150 requests/member/day
- Token lasts 2 months (5,184,000 seconds)

---

## Running & Testing

```bash
# Run the server
uv run mcp-server-linkedin

# Test with MCP Inspector
npx @modelcontextprotocol/inspector uv run mcp-server-linkedin
```
