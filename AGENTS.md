# AGENTS.md

Instructions for coding agents (Codex, Claude Code, etc.) working in this repository.

This file is the **canonical, tool-agnostic guide**. `CLAUDE.md` is a thin
companion file for Claude Code specifically — it points back here and adds only
what is unique to that tool. If guidance applies to every agent, it belongs
here, not in a companion file.

`CONTRIBUTING.md` is the authoritative reference for the branch/issue/PR
workflow and the full documentation policy. This file summarizes the parts an
agent needs day to day and defers to `CONTRIBUTING.md` for the rest.

## Project overview

This repository contains `pydplus`, a Python package/toolset for interacting with an RSA ID Plus tenant.

Primary goals when making changes:
- Keep the public API stable unless the change explicitly requires a breaking change.
- Prefer small, testable changes.
- Keep docs and docstrings consistent and Sphinx-friendly.

## Dev environment

Use Poetry for dependency management and packaging.

Common commands (prefer these unless the user asks otherwise):
- Install: `poetry install`
- Run tests: `poetry run pytest`
- Test suite location: `tests/unit/` and `tests/integration/` (repository root)
- Lint: `poetry run ruff check .`
- Format: `poetry run ruff format .`
- Format check (what CI runs): `poetry run ruff format --check .`
- Build: `poetry build`

If you add a dependency, add it via Poetry (`poetry add ...` / `poetry add --group dev ...`) rather than 
editing `pyproject.toml` by hand, and regenerate `poetry.lock` through Poetry.

## Files not to edit by hand

- `poetry.lock` — regenerate via Poetry.
- `src/pydplus.egg-info/` — build-generated.
- `dist/`, `.coverage`, `coverage.xml`, `.ruff_cache/`, `.pytest_cache/` — generated.
- `docs/_build/` — generated Sphinx output.

## Secrets and local-only files

This project authenticates against real RSA ID Plus tenants. Treat the following
as **off-limits** — never open, print, echo, paste into code/docs/commit
messages, or otherwise surface their contents, and never add real credentials
to any tracked file:

- `local/` — untracked; contains real helper configuration files, private keys,
  and other tenant-specific material.
- `.env` — untracked local environment file; `.env.example` is the tracked,
  placeholder-only template.
- `.github/scripts/decrypt_helper.sh` / `encrypt_secret.sh` — manage encrypted
  helper files used by CI; do not run or modify them unless explicitly asked.

When you need a configuration reference, use `examples/helper_example.json`,
which contains only placeholder values. Documentation and code examples must
use obviously fake placeholder values for tenant names, base URLs, client IDs,
client secrets, and keys/tokens.

## Python version support

The `pydplus` package supports Python **3.12, 3.13, and 3.14** (see `requires-python`
in `pyproject.toml` and the CI matrix in `.github/workflows/ci.yml`). Do not
add code that targets older Python versions, and do not silently narrow or
widen this support range (e.g. adding 3.15 support, or dropping 3.12) without
explicit authorization from a package maintainer.

## Coding style

- Prefer clarity over cleverness.
- Keep functions small and focused.
- Avoid unnecessary abstraction.
- Keep changes localized; don’t reformat unrelated code.
- Use type hints where they improve readability and tooling, especially for public APIs.
  - Type hints should be compatible with Python 3.12 and above.
- Follow the existing module layout: core client in `core.py`, low-level request/
  auth helpers in `api.py` / `auth.py` / `credentials.py`, user-related
  functionality in `users.py`, shared utilities under `utils/`, errors under
  `errors/`, and package-wide constants in `constants.py`.

### Constants

- All constants should be centralized within the `constants.py` module.
- Constants should be added to the section of the `constants.py` module that makes the most logical/organizational
  sense, and multiple similar constants should be grouped within classes and then exported.
- Type hints should be used wherever applicable in the `constants.py` module.
- Modules throughout the package that leverage constants should use specify the import name as `const`.
  (e.g. `from . import constants as const`)

## Docstrings (PEP 257 + Sphinx/reST)

### PEP 257 essentials (what “good” looks like)

Follow PEP 257 conventions:
- Use triple double-quotes: """..."""
- One-line docstrings:
  - The summary is on one line and ends with a period.
  - Example: """Return the API version string."""
- Multi-line docstrings:
  - First line is a short summary (imperative mood is fine), ending with a period.
  - Blank line after the summary.
  - Then a more detailed description if needed.
- Docstrings describe “what/why”; code should show “how”.
- Keep docstrings updated when behavior changes.

### Sphinx/reST field list style (required)

Use Sphinx/reST field lists for parameters and returns:

- :param <name>: ...
- :type <name>: ... (only if the type is non-obvious or you’re not using type hints consistently)
- :returns: ...
- :rtype: ... (only if needed; type hints usually suffice)
- :raises <ExceptionType>: ...

If type hints are present and clear, you may omit :type: and :rtype:.

### Function/method docstring template

```python
def example(name: str, enabled: bool = True) -> int:
    """Compute the example value.

    Longer explanation if needed.

    :param name: The user-facing name to process.
    :param enabled: Whether to enable additional processing.
    :returns: The computed example value.
    :raises ValueError: If `name` is empty.
    """
```

### Package / module docstrings (including __init__.py)

#### Module docstrings (some_module.py)

Every public module should start with a module docstring describing purpose and key concepts:

```
"""
:Module:            pydplus.users
:Synopsis:          Defines the user-related functions associated with the RSA ID Plus API
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     07 Mar 2026
"""
```

#### Package docstrings (__init__.py)

If `src/pydplus/__init__.py` exposes the public API (re-exports classes/functions),
include a package docstring that explains the package purpose and lists key exports.

```
"""
:Module:            pydplus
:Synopsis:          This package provides the :py:class:`pydplus.PyDPlus` client and related helpers
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     09 Mar 2026
"""
```

### Class docstrings vs __init__ docstrings (important rule)

#### Preferred approach for user-facing classes

For user-facing classes, document constructor parameters in the class docstring (not duplicated in __init__), using :param: fields.

```python
class PyDPlus:
    """Class for the core client object that interfaces with the RSA REST APIs.

    :param connection_info: Dictionary that defines the connection info to use
    :type connection_info: dict, None
    :param connection_type: Determines whether to leverage a(n) ``oauth`` (default) or ``legacy`` connection
    :type connection_type: str, None
    :param base_url: The base URL to leverage when performing API calls
    :type base_url: str, None
    :param private_key: The file path to the private key used for API authentication (OAuth or Legacy)
    :type private_key: str, None
    :param legacy_access_id: The Access ID associated with the Legacy API connection
    :type legacy_access_id: str, None
    :param oauth_client_id: The Client ID associated with the OAuth API connection
    :type oauth_client_id: str, None
    :param verify_ssl: Determines if SSL connections should be verified (``True`` by default)
    :type verify_ssl: bool, None
    :param auto_connect: Determines if an API connection should be established when the object is instantiated
                         (``True`` by default)
    :type auto_connect: bool
    :param strict_mode: Determines if failed API responses should result in an exception being raised
                        (``False`` by default)
    :type strict_mode: bool, None
    :param env_variables: Optionally define custom environment variable names to use instead of the default names
    :type env_variables: dict, None
    :param helper: Optionally provide the file path for a helper file used to define the object configuration
    :type helper: str, tuple, list, set, dict, None
    :returns: The instantiated PyDPlus object
    :raises: :py:exc:`TypeError`
    """
    # Define the function that initializes the object instance (i.e. instantiates the object)
    def __init__(
            self,
            connection_info: Optional[dict] = None,
            connection_type: Optional[str] = None,
            base_url: Optional[str] = None,
            private_key: Optional[str] = None,
            legacy_access_id: Optional[str] = None,
            oauth_client_id: Optional[str] = None,
            verify_ssl: Optional[bool] = None,
            auto_connect: bool = True,
            strict_mode: Optional[bool] = None,
            env_variables: Optional[dict] = None,
            helper: Union[Optional[str], Optional[tuple], Optional[list], Optional[set], Optional[dict]] = None,
    ):
        """Instantiate the core client object.
        
        Parameter documentation is defined on the class docstring.
        """
```

#### When __init__ should have full :param: docs

Only put full :param: documentation on __init__ if:
- the class docstring is intentionally minimal, or
- the class is internal/private and only __init__ needs documentation, or
- you need to document multiple alternative init signatures/behaviors that are clearer at __init__.

### Properties

Use property docstrings as short descriptions. Avoid :param: fields (properties take no params).

```python
@property
def api_version(self) -> str:
    """The RSA REST API version in use."""
```

## Tests

- Test suites live at the repository root under `tests/unit/` and `tests/integration/`.
- Add or update tests for behavior changes; add a regression test for every bug fix.
- Prefer pytest-style tests.
- Keep tests deterministic (no real network calls unless explicitly requested).
- Integration tests are opt-in: they are skipped by default and only run with
  `poetry run pytest --run-integration tests/integration -q`. Do not attempt to
  run them without a real (or appropriately mocked) helper/tenant configuration.
  For releases, integration validation is recommended when an authorized ID Plus
  test environment is available, but may be skipped with a recorded reason when
  access is not feasible; that skip does not block release readiness.

## Documentation expectations

- If you change a public behavior, update the docstrings and any relevant docs under `docs/` (always the `CHANGELOG.md` file).
- When creating a new module, a header block similar to the example below should be included.

```python
# -*- coding: utf-8 -*-
"""
:Module:            pydplus.new_module_name
:Synopsis:          Defines the functionality related to ????
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     27 Feb 2026
"""
```

- If you change any file with a header block containing `Last Modified` or `Modified Date` fields:
  - Update the `Last Modified` field with the name (or username/pseudonym) of the person making the change.
    - The person making the change indicates the human developer who is orchestrating the AI-generated changes.
    - If the person does not wish to display their name/username/pseudonym, use "Anonymous" as the value. Otherwise, 
      default to displaying their name (preferred) or username from their GitHub profile.
    - Indicate after the value which AI tool and/or model was utilized (e.g. `John Doe (via GPT-5.3-Codex)`, `johndoe434 (via claude-opus-4-5)`, etc.)
  - Update the `Modified Date` field where applicable with the current date (local time) in the same format as the existing value.
- Keep examples accurate and runnable.

## Branch, commit, and PR hygiene

`CONTRIBUTING.md` has the full rules (branch prefixes, required Issue linkage,
PR requirements); the essentials:

- Branch from `main`; never commit directly to `main`.
- Branch names must include the GitHub Issue number and use one of the valid
  prefixes (`feature/`, `fix/`, `refactor/`, `chore/`, `docs/`, `test/`, `ci/`,
  `security/`) — see `CONTRIBUTING.md` for the full convention.
- Do not commit or push unless the user asks.
- Keep commits focused and descriptive and prefer past-tense over present-tense. ("Updated the ..." over "Update the ...")
- Explicitly mention the file name if it fits organically and does not distract from the commit message itself.
- Avoid large refactors unless requested.
- Don’t change formatting in unrelated files.
- Every PR should reference a GitHub Issue and use the matching branch prefix.
- For suspected vulnerabilities, use GitHub Private Vulnerability Reporting —
  do not open a public issue or include exploit details, payloads, or secrets.

## Security

`pydplus` handles authentication flows and API tokens/keys for RSA ID Plus.
Contributions must (see `CONTRIBUTING.md` → "Security Expectations" for the
full policy):

- Never log secrets (client IDs/secrets, private keys, JWTs, session tokens).
- Avoid insecure defaults; keep SSL verification on by default.
- Validate user input where applicable.
- Justify any cryptographic or authentication change.
- Keep security-sensitive dependency floors (see the pinned versions and
  comments in `pyproject.toml`) intact or higher.
- CI runs Bandit (`poetry run bandit -r src`) for static security analysis;
  don't introduce findings it would flag.

## Pre-submit checklist

Before handing work back or opening a PR:

1. `poetry run ruff check .`
2. `poetry run ruff format --check .`
3. `poetry run pytest -q`
4. Docstrings and `docs/` updated for any public-behavior change.
5. `docs/CHANGELOG.md` updated for any user-facing change.
6. Header blocks (`Last Modified` / `Modified Date`) updated on changed files only.
7. No secrets or real credentials added to tracked files.
