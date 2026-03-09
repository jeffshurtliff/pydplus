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

## Coverage

Coverage is enabled via pytest defaults in `pyproject.toml` and generated on each run.
To run all tests (including integration) with coverage:

```bash
poetry run pytest --run-integration --cov=pydplus --cov-report=term-missing --cov-report=xml
```
