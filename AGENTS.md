# AGENTS.md

Instructions for coding agents (Codex, etc.) working in this repository.

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
- Test suite location: `tests/` (repository root)
- Lint/format (if configured in this repo): `poetry run ruff check .` and `poetry run ruff format .`
- Build: `poetry build`

If you add a dependency, add it via Poetry (`poetry add ...` / `poetry add --group dev ...`) rather than 
editing `pyproject.toml` by hand.

## Python version support

The `pydplus` package is intended to support Python versions 3.9 and above. Support for version 3.9 should
**not** be removed (i.e, requiring 3.10+) unless there is a critical need to do so, such as a high-severity 
security vulnerability that requires 3.10 or higher to patch, crucial functionality cannot be implemented, 
or similar situations. Agents should never remove 3.9 support unilaterally without explicit authorization 
from a package maintainer.

## Coding style

- Prefer clarity over cleverness.
- Keep functions small and focused.
- Avoid unnecessary abstraction.
- Keep changes localized; don’t reformat unrelated code.
- Use type hints where they improve readability and tooling, especially for public APIs.
  - Type hints should be compatible with Python 3.9 and above.

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

- Add or update tests for behavior changes.
- Prefer pytest-style tests.
- Keep tests deterministic (no real network calls unless explicitly requested).

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

## PR / commit hygiene (if applicable)

- Keep commits focused and descriptive and prefer past-tense over present-tense. ("Updated the ..." over "Update the ...")
- Explicitly mention the file name if it fits organically and does not distract from the commit message itself.
- Avoid large refactors unless requested.
- Don’t change formatting in unrelated files.
