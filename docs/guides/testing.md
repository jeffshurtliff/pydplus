# Testing

PyDPlus tests are found in the `tests/` directory within the repository.

## Run the Test Suite

Install dependencies and run all tests:

```bash
poetry install
poetry run pytest -q
```

## Coverage

Run coverage locally with:

```bash
poetry run pytest --cov-report=xml --cov=pydplus tests --color=yes
```
