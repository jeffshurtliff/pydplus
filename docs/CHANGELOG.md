# Changelog

This project uses a curated changelog to highlight notable changes by release.
Detailed commit history remains available in GitHub.

The format is based on the [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) guidelines,
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---
(relnotes-unreleased)=
## [Unreleased]

(unreleased-added)=
### Added

No unreleased additions at this time.

(unreleased-changed)=
### Changed

No unreleased changes at this time.

---
(relnotes-1.0.0)=
## [1.0.0] - 2026-04-02

This was the first release of the `pydplus` package on PyPI with its original 
features and functionality.

### Added

- Added shared pytest fixtures and integration-test controls in `tests/conftest.py`.
- Added unit tests in `tests/unit/test_logging.py` for `pydplus.utils.log_utils`.
- Added secure RSA ID Plus legacy credential parsing and explicit PEM persistence helpers in `src/pydplus/credentials.py`.
- Added `IDPlusCredentialError` in `src/pydplus/errors/exceptions.py` for credential parsing and key-material handling failures.
- Added OAuth Private Key JWT support for Administration API connections in `src/pydplus/auth.py`.
- Added OAuth token caching and one-time 401 refresh/retry handling in `src/pydplus/api.py`.
- Added OAuth unit coverage in `tests/unit/test_auth.py` and `tests/unit/test_api_oauth.py`.
- Added OAuth scope normalization helpers and strict scope-validation coverage in `tests/unit/test_core_utils.py`.

### Changed

- Refactored tests into `tests/unit/` and `tests/integration/` with updated testing documentation and default coverage reporting.
- Adopted Ruff for linting, import sorting, and formatting; added Ruff configuration in `pyproject.toml`; replaced the CI flake8 step with Ruff check/format validation; set the line-length standard to 130 characters; and documented targeted `E501` override guidance for comment/special-case lines.
- Documented the Requests `extract_zipped_paths()` advisory triage: PyDPlus does not call the affected utility, maintainers should dismiss the related Dependabot alert as not affected, and runtime environments should set `TMPDIR` to a restricted-write directory where applicable.
- Updated `pygments` from `2.19.1` to `2.19.2` (latest available) and documented risk-limiting guidance for the low-severity ReDoS advisory affecting lexer behavior in documentation tooling paths.
- Updated `cryptography` minimum version to `46.0.6` to remediate the name-constraint enforcement advisory affecting peer-name validation.
- Updated `pydplus.utils.log_utils` with comprehensive type hints/docstrings and improved handler/level configuration behavior.
- Updated `pydplus.core.PyDPlus` to accept legacy key material (parsed object or `.key` path) and wire it into legacy connection initialization.
- Updated legacy auth private-key loading to support in-memory PEM data from connection info in addition to file paths.
- Refactored package-module logging to use `logging.getLogger(__name__)` without import-time self-configuration and updated development logging guidance/helpers accordingly.
- Updated `pydplus.core.PyDPlus` and `compile_connection_info()` to support OAuth private-key JWK configuration via arguments, helper settings, and environment variables.
- Updated connection-type resolution to preserve explicit values and auto-detect complete OAuth/Legacy credential sets before defaulting.
- Updated helper/environment constant mappings to include OAuth private-key path, file, and inline JWK fields.
- Added explicit `oauth_issuer_url` support and updated OAuth issuer inference defaults to prefer Authentication API hosts for `/oauth/token` requests, while retaining `oauth_api_type` overrides.
- Updated OAuth client-credentials handling to require explicit scopes, accept `+`-delimited/space-delimited/iterable scope inputs, normalize internally to `+`-delimited values, send space-delimited `scope` values to `/oauth/token` with explicit form content-type, validate against `const.OAUTH_SCOPES`, and include scope-aware token caching behavior.
- Updated OAuth scope-preset handling so helper files define presets under `connection.oauth.scope_preset`, environment variables use `PYDPLUS_OAUTH_SCOPE_PRESET`, and presets are merged additively with explicit scopes instead of replacing them.
- Updated `pydplus.utils.core_utils.get_random_string()` to use the `secrets` module for cryptographically secure random string generation.


<!-- The reference definitions are listed below -->
[Unreleased]: https://github.com/jeffshurtliff/pydplus/compare/1.0.0...HEAD
[1.0.0]: https://github.com/jeffshurtliff/pydplus/releases/tag/1.0.0
