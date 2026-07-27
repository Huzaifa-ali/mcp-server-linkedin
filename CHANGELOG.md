# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2025-07-27

### Changed

- **Architecture:** Full modular refactor with single-responsibility modules
- **Service layer:** `LinkedInService` with shared `httpx.AsyncClient` and connection pooling
- **Models:** Frozen dataclass models (`LinkedInProfile`, `PostResult`, `MediaUploadInfo`) with `from_api_response()` factories
- **Exceptions:** Typed exception hierarchy (`LinkedInAPIError`, `AuthenticationError`, `MediaUploadError`, `ConfigurationError`, `ValidationError`)
- **Tool registration:** Direct `mcp.tool()` binding — removed redundant wrapper layer
- **Config:** Split into pure `config.py` (constants) and `utils/token.py` (file I/O)
- **Settings:** `LinkedInSettings` is now a frozen dataclass with `slots=True`

### Added

- `src/mcp_server_linkedin/models/` — typed API response models
- `src/mcp_server_linkedin/services/` — async API client with connection pooling
- `src/mcp_server_linkedin/utils/` — token persistence utilities
- `src/mcp_server_linkedin/exceptions.py` — structured exception hierarchy
- `.pre-commit-config.yaml` — Ruff + mypy pre-commit hooks
- `pyproject.toml` dev dependencies (ruff, mypy, pytest, pytest-asyncio, pre-commit)
- `pyproject.toml` tool configuration (ruff, mypy, pytest, coverage)

### Removed

- `linkedin_client.py` — replaced by `services/linkedin.py`
- Wrapper functions in `server.py` — tools now register directly

## [0.1.0] - 2025-01-01

### Added

- Initial release
- OAuth 2.0 authentication with browser-based flow
- Text post publishing
- Image post publishing (register + upload + publish)
- Video post publishing (register + upload + publish)
- Article/link post publishing with preview
- Post deletion
- Profile retrieval
- Stubbed analytics tools (pending Community Management API)
- Configuration for Claude Desktop, Kiro, Cursor, VS Code, Windsurf, Claude Code
