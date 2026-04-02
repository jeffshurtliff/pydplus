# Testing

PyDPlus tests are located in the `tests/` directory and split by scope:

- `tests/unit/`: fast, isolated tests for individual units of functionality
- `tests/integration/`: higher-level tests that validate behavior across modules
- `tests/conftest.py`: shared fixtures and pytest hooks used by both test suites

## Run the Test Suite

Install dependencies and run the default suite (unit tests):

```bash
poetry install
poetry run pytest -q
```

Integration tests are opt-in and skipped by default. To run them:

```bash
poetry run pytest --run-integration -m integration -q
```

## Linting and Formatting

This project uses Ruff for linting, import sorting, and formatting.
The repository line-length standard is `130` characters.

Use line-length overrides only for comments or special situations where wrapping harms readability.
Prefer targeted per-line `# noqa: E501` over broad file-level or global ignores.

```bash
poetry run ruff check .
poetry run ruff check . --fix
poetry run ruff format .
poetry run ruff format . --check
```

## Coverage

Coverage is enabled via pytest defaults in `pyproject.toml` and generated on each run.
To run all tests (including integration) with coverage:

```bash
poetry run pytest --run-integration --cov=pydplus --cov-report=term-missing --cov-report=xml
```

## Security Notes for Documentation Tooling

`pygments` is used in this repository for documentation rendering via Sphinx, not
for `pydplus` runtime request/response processing.

For documentation-tooling security hygiene (including the ReDoS advisory patched in `pygments>=2.20.0`):

- Keep `pygments` at the newest available version in the lock file.
- Only build docs from trusted repository content.
- Do not run ad-hoc syntax highlighting on untrusted input as part of local scripts or CI jobs.
- If your CI platform supports it, run documentation builds with a job timeout and isolated resources.
