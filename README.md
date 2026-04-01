<img src="docs/_static/pydplus-icon-cropped.png"
     class="pydplus-c-landing-page-logo" 
     style="background-color: transparent; max-height: 320px;"
     alt="PyDPlus Logo" />

# PyDPlus
A Python toolset for the RSA ID Plus cloud authentication platform.

<table>
    <tr>
        <td>Latest Stable Release</td>
        <td>
            <a href="https://pypi.org/project/pydplus/">
                <img alt="PyPI" src="https://img.shields.io/pypi/v/pydplus">
            </a>
        </td>
    </tr>
    <tr>
        <td>Latest Beta/RC Release</td>
        <td>
            <a href="https://pypi.org/project/pydplus/#history">
                <img alt="PyPI" src="https://img.shields.io/badge/pypi-1.0.0b1-blue">
            </a>
        </td>
    </tr>
    <tr>
        <td>Build Status</td>
        <td>
            <a href="https://github.com/jeffshurtliff/pydplus/blob/main/.github/workflows/ci.yml">
                <img alt="GitHub Workflow Status" 
                src="https://img.shields.io/github/actions/workflow/status/jeffshurtliff/pydplus/ci.yml?branch=main">
            </a>
        </td>
    </tr>
    <tr>
        <td>Supported Versions</td>
        <td>
            <a href="https://pypi.org/project/pydplus/">
                <img alt="PyPI - Python Versions Supported" src="https://img.shields.io/pypi/pyversions/pydplus">
            </a>
        </td>
    </tr>
    <tr>
        <td>Code Coverage</td>
        <td>
            <a href="https://codecov.io/gh/jeffshurtliff/pydplus">
                <img alt="Codecov - Code Coverage" src="https://codecov.io/gh/jeffshurtliff/pydplus/branch/main/graph/badge.svg?token=QBynJO48jN" />
            </a>
        </td>
    </tr>
    <tr>
        <td>Documentation</td>
        <td>
            <a href="https://pydplus.readthedocs.io/en/latest/?badge=latest">
                <img alt="Documentation Status" src="https://readthedocs.org/projects/pydplus/badge/?version=latest" />
            </a>
        </td>
    </tr>
    <tr>
        <td>Security Audits</td>
        <td>
            <a href="https://github.com/marketplace/actions/python-security-check-using-bandit">
                <img alt="Bandit" src="https://img.shields.io/badge/security-bandit-yellow.svg">
            </a>
        </td>
    </tr>
    <tr>
        <td>License</td>
        <td>
            <a href="https://github.com/jeffshurtliff/pydplus/blob/main/LICENSE">
                <img alt="License (GitHub)" src="https://img.shields.io/github/license/jeffshurtliff/pydplus">
            </a>
        </td>
    </tr>
    <tr>
        <td style="vertical-align: top;">Issues</td>
        <td>
            <a href="https://github.com/jeffshurtliff/pydplus/issues">
                <img style="margin-bottom:5px;" alt="GitHub Open Issues" src="https://img.shields.io/github/issues-raw/jeffshurtliff/pydplus"><br />
            </a>
            <a href="https://github.com/jeffshurtliff/pydplus/issues">
                <img alt="GitHub Closed Issues" src="https://img.shields.io/github/issues-closed-raw/jeffshurtliff/pydplus">
            </a>
        </td>
    </tr>
    <tr>
        <td style="vertical-align: top;">Pull Requests</td>
        <td>
            <a href="https://github.com/jeffshurtliff/pydplus/pulls">
                <img style="margin-bottom:5px;" alt="GitHub Open Pull Requests" src="https://img.shields.io/github/issues-pr-raw/jeffshurtliff/pydplus"><br />
            </a>
            <a href="https://github.com/jeffshurtliff/pydplus/pulls">
                <img alt="GitHub Closed Pull Requests" src="https://img.shields.io/github/issues-pr-closed-raw/jeffshurtliff/pydplus">
            </a>
        </td>
    </tr>
</table>

## Installation
Install from PyPI:

```sh
python -m pip install --upgrade pydplus
```

Install from source:

```sh
git clone https://github.com/jeffshurtliff/pydplus.git
cd pydplus
poetry install
```

## Change Log
The change log can be found in the [documentation](https://pydplus.readthedocs.io/en/latest/CHANGELOG.html).

## Usage
PyDPlus is designed for Python-based administration workflows in RSA ID Plus tenants, including:

- user lifecycle automation (lookup, disable, mark for deletion)
- admin reporting and audit integrations
- helpdesk and identity-operations scripting

### 1) Import the package

```python
from pydplus import PyDPlus, constants as const
```

### 2) Instantiate the client (OAuth example)

`pydplus.PyDPlus` supports both OAuth and Legacy credentials. OAuth (Private Key JWT) is recommended for new usage.

```python
from pydplus import PyDPlus, constants as const

OAUTH_SCOPE = [
    const.OAUTH_SCOPES.USER_READ,
    const.OAUTH_SCOPES.USER_MANAGE,
]

pydp = PyDPlus(
    connection_type="oauth",
    base_admin_url="https://example-company.access.securid.com",
    oauth_client_id="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
    oauth_private_key="/path/to/oauth-private-key.jwk",
    oauth_scope=OAUTH_SCOPE,
)
```

Legacy API authentication is also supported. See the 
[Authentication](https://pydplus.readthedocs.io/en/latest/guides/authentication.html) guide for both patterns.

### 3) Define OAuth scopes (three practical options)

1. Configure default scope permissions in the OAuth client settings in the RSA Cloud Administration Console.
2. Define scopes explicitly in your code/helper/env configuration (manual string values or constants like
   `const.OAUTH_SCOPES.USER_READ` grouped in an `OAUTH_SCOPE` variable).
3. Use `oauth_scope_preset` to apply scope bundles (for example `user_read_only` or `group_read_only`).

In PyDPlus, keep `oauth_scope` explicitly defined (directly, helper file, or environment variable) so token requests
remain deterministic and validated.

Presets are additive and merged with explicit scopes:

```python
pydp = PyDPlus(
    connection_type="oauth",
    base_admin_url="https://example-company.access.securid.com",
    oauth_client_id="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
    oauth_private_key="/path/to/oauth-private-key.jwk",
    oauth_scope=const.OAUTH_SCOPES.USER_MANAGE,
    oauth_scope_preset=("user_read_only", "group_read_only"),
)
```

### 4) Run an API operation

```python
user_id = pydp.users.get_user_id(email="john.doe@example.com")
response = pydp.users.disable_user(user_id=user_id)
```

For deeper coverage, see:

- Quickstart: <https://pydplus.readthedocs.io/en/latest/getting-started/quickstart.html>
- Authentication guide: <https://pydplus.readthedocs.io/en/latest/guides/authentication.html>
- Client reference: <https://pydplus.readthedocs.io/en/latest/reference/client.html>

## Documentation
The documentation is located here: [https://pydplus.readthedocs.io/en/latest/](https://pydplus.readthedocs.io/en/latest/)

## License
[MIT License](https://github.com/jeffshurtliff/pydplus/blob/main/LICENSE)

## Reporting Issues
Issues can be reported within the [GitHub repository](https://github.com/jeffshurtliff/pydplus/issues).

## Contributing
Contributions are welcome and appreciated, including bug fixes, documentation improvements, tests, and feature work.
For full contribution requirements and workflows, please see
[CONTRIBUTING.md](https://github.com/jeffshurtliff/pydplus/blob/main/CONTRIBUTING.md).

### Development Quality Checks
This repository uses [Ruff](https://docs.astral.sh/ruff/) for linting, import sorting, and formatting.
The standard maximum line length for this package is `130` characters.

Line-length exceptions should be rare and limited to comments or special cases where wrapping harms readability.
When an exception is required, use a targeted per-line `# noqa: E501` comment.

```sh
poetry run ruff check .
poetry run ruff check . --fix
poetry run ruff format .
poetry run ruff format . --check
```

These checks are enforced in CI via `.github/workflows/ci.yml`.

## Donations
If you would like to donate to this project then you can do so using [this PayPal link](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=XDZ8M6UV6EFK6&item_name=PyDPlus+Python+SDK&currency_code=USD).

## Disclaimer
This package is considered unofficial and is in no way endorsed or supported by [RSA Security LLC](https://rsa.com).
