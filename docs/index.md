<img src="_static/pydplus-icon-cropped.png"
     class="pydplus-c-landing-page-logo" 
     style="background-color: transparent; max-height: 320px;"
     alt="PyDPlus Logo" />

# PyDPlus Documentation

PyDPlus is a Python package for working with RSA APIs through a single, 
high-level client. This documentation covers setup, authentication patterns,
query workflows, error handling, and the complete API reference.

```{toctree}
:maxdepth: 1
:hidden:

getting-started/index
guides/index
reference/index
CHANGELOG
```

## At A Glance

- Purpose: Simplify RSA REST API interactions in Python
- Primary interface: `pydplus.PyDPlus`
- Supported Python versions: 3.9+
- License: MIT

## What You Can Do

With PyDPlus, you can:

- Authenticate against RSA ID Plus tenants
- Retrieve user details
- Manage user status and mark them for deletion

## Installation

```bash
pip install --upgrade pydplus
```

## Quick Example

```python
from pydplus import PyDPlus

pydp = PyDPlus(helper="/path/to/helper.yml")

user_id = pydp.users.get_user_id(email='john.doe@edample.com')
print(user_id)
```

For a complete walkthrough, see the {doc}`getting-started/quickstart` page.

## Documentation Map

### Getting Started

- {doc}`getting-started/overview`: Package capabilities and requirements
- {doc}`getting-started/installation`: Installation and environment setup
- {doc}`getting-started/quickstart`: Minimal end-to-end usage example

### Guides

- {doc}`guides/authentication`: Credential patterns and helper-file usage
- {doc}`guides/error-handling`: Exceptions, diagnostics, and recovery patterns
- {doc}`guides/testing`: Running tests from `tests/`

### API Reference

- {doc}`reference/client`: `PyDPlus` class and client-facing modules
- {doc}`reference/utilities`: Utility functions and helpers
- {doc}`reference/exceptions`: Exception classes and error helpers

### Project Information

- {doc}`CHANGELOG`: Release history and notable changes

## Project Links

- Source code: <https://github.com/jeffshurtliff/pydplus>
- Package index: <https://pypi.org/project/pydplus/>
- Issue tracker: <https://github.com/jeffshurtliff/pydplus/issues>

## Disclaimer

This package is considered unofficial and is in no way endorsed or 
supported by [RSA Security LLC](https://rsa.com).
