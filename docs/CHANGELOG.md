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

(unreleased-changed)=
### Changed

- Refactored tests into `tests/unit/` and `tests/integration/` with updated testing documentation and default coverage reporting.
- Updated `pydplus.utils.log_utils` with comprehensive type hints/docstrings and improved handler/level configuration behavior.

---
(relnotes-1.0.0)=
## [1.0.0] - 2026-MM-DD

This was the first release of the `pydplus` package on PyPI with its original 
features and functionality.


<!-- The reference definitions are listed below -->
[Unreleased]: https://github.com/jeffshurtliff/salespyforce/compare/1.0.0...HEAD
[1.0.0]: https://github.com/jeffshurtliff/salespyforce/releases/tag/1.0.0
