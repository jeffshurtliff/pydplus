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

- Added shared pytest fixtures and integration-test controls in `tests/conftest.py`.
- Added unit tests in `tests/unit/test_logging.py` for `pydplus.utils.log_utils`.
- Added secure RSA ID Plus legacy credential parsing and explicit PEM persistence helpers in `src/pydplus/credentials.py`.
- Added `IDPlusCredentialError` in `src/pydplus/errors/exceptions.py` for credential parsing and key-material handling failures.
- Added OAuth Private Key JWT support for Administration API connections in `src/pydplus/auth.py`.
- Added OAuth token caching and one-time 401 refresh/retry handling in `src/pydplus/api.py`.
- Added OAuth unit coverage in `tests/unit/test_auth.py` and `tests/unit/test_api_oauth.py`.

(unreleased-changed)=
### Changed

- Refactored tests into `tests/unit/` and `tests/integration/` with updated testing documentation and default coverage reporting.
- Updated `pydplus.utils.log_utils` with comprehensive type hints/docstrings and improved handler/level configuration behavior.
- Updated `pydplus.core.PyDPlus` to accept legacy key material (parsed object or `.key` path) and wire it into legacy connection initialization.
- Updated legacy auth private-key loading to support in-memory PEM data from connection info in addition to file paths.
- Refactored package-module logging to use `logging.getLogger(__name__)` without import-time self-configuration and updated development logging guidance/helpers accordingly.
- Updated `pydplus.core.PyDPlus` and `compile_connection_info()` to support OAuth private-key JWK configuration via arguments, helper settings, and environment variables.
- Updated connection-type resolution to preserve explicit values and auto-detect complete OAuth/Legacy credential sets before defaulting.
- Updated helper/environment constant mappings to include OAuth private-key path, file, and inline JWK fields.
- Added explicit `oauth_issuer_url` support and updated OAuth issuer inference defaults to prefer Authentication API hosts for `/oauth/token` requests, while retaining `oauth_api_type` overrides.

---
(relnotes-1.0.0)=
## [1.0.0] - 2026-MM-DD

This was the first release of the `pydplus` package on PyPI with its original 
features and functionality.


<!-- The reference definitions are listed below -->
[Unreleased]: https://github.com/jeffshurtliff/salespyforce/compare/1.0.0...HEAD
[1.0.0]: https://github.com/jeffshurtliff/salespyforce/releases/tag/1.0.0
