# Development Utilities

This directory contains helper utilities intended to support local development, debugging, and testing 
of the `pydplus` package. These utilities are **not part of the public API** and should not be relied 
upon by external consumers of the package.

---

## `dev_logging.py`

### Overview

The `dev_logging.py` module provides a simple, consistent way to enable debug-friendly logging when 
developing or troubleshooting the `pydplus` package.

It wraps the core logging configuration provided by:

```
pydplus.utils.log_utils.initialize_logging()
```

and applies sensible defaults for development scenarios.

---

## Why use this helper?

By default, the `pydplus` logging utility attaches a `NullHandler` unless output is explicitly enabled. 
This is ideal for library usage, but it can make development confusing because no logs appear in the console.

The `setup_dev_logging()` helper solves this by:

- Enabling console logging by default
- Enabling debug-level logging across all handlers
- Optionally enabling file logging
- Providing a consistent logging configuration across all development scripts

---

## Basic Usage

Import and initialize logging at the top of your script:

```python
from dev.dev_logging import setup_dev_logging

logger = setup_dev_logging(__name__)
```

You can then use the logger as usual:

```python
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

---

## Running a Script

Example:

```bash
python3 update_users.py
```

With the default configuration:

- `DEBUG` and `INFO` messages are sent to `stdout`
- `WARNING` and above are sent to `stderr`
- All messages are visible in the terminal

---

## Enabling File Logging

To persist logs to a file:

```python
logger = setup_dev_logging(
    __name__,
    file=True,
    log_file="./logs/update_users.log",
)
```

### Notes

- If `file=True` and `log_file` is not provided, logs default to:
  ```
  ./pydplus-dev.log
  ```
- If a relative path is provided (e.g. `./logs/...`), it will be created if it does not exist
- Log files are overwritten by default (`overwrite=True`)

---

## Configuration Options

```python
setup_dev_logging(
    logger_name: str,
    *,
    debug: bool = True,
    console: bool = True,
    file: bool = False,
    log_file: Optional[str] = None,
    overwrite: bool = True,
)
```

### Parameters

| Parameter     | Description                                   |
|---------------|-----------------------------------------------|
| `logger_name` | Logger name (typically `__name__`)            |
| `debug`       | Enables debug-level logging for all handlers  |
| `console`     | Enables console output (stdout/stderr)        |
| `file`        | Enables file logging                          |
| `log_file`    | Path to the log file (optional)               |
| `overwrite`   | Whether to overwrite the log file on each run |

---

## Recommended Development Patterns

### Standard Development

```python
logger = setup_dev_logging(__name__)
```

### Debugging with File Output

```python
logger = setup_dev_logging(
    __name__,
    file=True,
    log_file="./logs/debug.log",
)
```

### Quiet Mode (Library Behavior)

If you want to disable development logging and revert to library-style behavior:

```python
from pydplus.utils import log_utils

logger = log_utils.initialize_logging(__name__)
```

---

## Scope and Intent

This helper is intended for:

- Local development
- Debugging scripts
- Interactive sessions (e.g., IDLE, PyCharm console)
- Troubleshooting API interactions

This helper is **not intended for production use**.

---

## Future Enhancements (Optional)

Maintainers may consider extending this helper with:

- Environment variable support (e.g., `PYDPLUS_DEBUG`)
- CLI flags (e.g., `--debug`, `--log-file`)
- Predefined logging profiles (e.g., `dev`, `quiet`, `debug`)

---

## Summary

Use `setup_dev_logging()` whenever you want immediate visibility into what the package is doing during development. 
It provides a consistent, low-friction way to enable logging without modifying core package behavior.
