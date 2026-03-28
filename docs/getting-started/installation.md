# Installation

This page explains how to install `pydplus` either from PyPI using `pip` or
from source by cloning the repository and building a wheel with `poetry`.
For prerequisites (Python version, Salesforce org access, API permissions), see
the [Overview](overview.md).

## Install With `pip`

Use `pip` when you want the simplest setup and you are not modifying the code.

```bash
python -m pip install --upgrade pip
python -m pip install pydplus
```

To verify the installation:

```bash
python -c "import pydplus; print(pydplus.__version__)"
```

## Install From Source (Build With `poetry`)

Use this approach if you plan to contribute, need unreleased changes, or want to
inspect the code.

1. Clone the repository.

```bash
git clone https://github.com/jeffshurtliff/pydplus.git
cd pydplus
```

2. Install dependencies with Poetry.

```bash
poetry install
```

3. Build the distribution artifacts (wheel and source distribution).

```bash
poetry build
```

4. Install the built wheel with `pip`.

```bash
python -m pip install dist/*.whl
```

If you prefer to use the package in editable mode while developing, you can
install it directly from the repository with Poetry’s environment:

```bash
poetry run python -m pip install -e .
```

## Troubleshooting

If installation fails due to missing Python or environment issues, revisit the
requirements on the [Overview](overview.md) page and confirm your Python version
matches the supported range.

### Temporary Directory Hardening (`TMPDIR`)

`pydplus` does not call `requests.utils.extract_zipped_paths()` directly, but if
your runtime environment enforces conservative hardening for temporary-file use,
you can set `TMPDIR` to a directory with restricted write access.

Example (Linux/macOS):

```bash
mkdir -p "${HOME}/.tmp/pydplus"
chmod 700 "${HOME}/.tmp/pydplus"
export TMPDIR="${HOME}/.tmp/pydplus"
```

In CI, set `TMPDIR` in the job environment before running tests or scripts.
