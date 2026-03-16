# -*- coding: utf-8 -*-
"""
:Module:            tests.unit.test_logging
:Synopsis:          Unit tests for pydplus.utils.log_utils
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff (via GPT-5.3-codex)
:Modified Date:     16 Mar 2026
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from uuid import uuid4

import pytest

from pydplus.utils import log_utils


pytestmark = pytest.mark.unit


def _get_clean_logger() -> logging.Logger:
    """Return a logger with no attached handlers."""
    logger_name = f'tests.unit.log_utils.{uuid4().hex}'
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.NOTSET)
    logger.propagate = True
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()
    return logger


def test_initialize_logging_adds_null_handler_by_default_and_is_idempotent() -> None:
    """Ensure default initialization adds only one null handler across repeated calls."""
    logger_name = f'tests.unit.log_utils.default.{uuid4().hex}'
    logger = log_utils.initialize_logging(logger_name=logger_name)
    logger = log_utils.initialize_logging(logger_name=logger_name)

    assert logger.level == logging.INFO
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.NullHandler)


def test_initialize_logging_replaces_managed_handlers_without_removing_user_handlers() -> None:
    """Ensure repeated initialization does not duplicate managed handlers."""
    logger_name = f'tests.unit.log_utils.managed.{uuid4().hex}'
    logger = logging.getLogger(logger_name)
    logger.addHandler(logging.StreamHandler())

    logger = log_utils.initialize_logging(
        logger_name=logger_name,
        console_output=True,
        console_log_level='error',
    )
    logger = log_utils.initialize_logging(
        logger_name=logger_name,
        console_output=True,
        console_log_level='error',
    )

    managed_handlers = [
        handler for handler in logger.handlers if getattr(handler, log_utils.MANAGED_HANDLER_ATTR, False)
    ]
    unmanaged_handlers = [
        handler for handler in logger.handlers if not getattr(handler, log_utils.MANAGED_HANDLER_ATTR, False)
    ]

    assert len(managed_handlers) == 1
    assert len(unmanaged_handlers) == 1


def test_apply_defaults_enables_debug_and_converts_formatter_strings() -> None:
    """Ensure debug mode forces debug levels and converts formatter strings."""
    logger_name, log_levels, formatter = log_utils._apply_defaults(
        _logger_name=None,
        _formatter='%(levelname)s:%(message)s',
        _debug=True,
        _log_level=None,
        _file_level=None,
        _console_level=None,
        _syslog_level=None,
    )

    assert logger_name == log_utils.LOGGING_DEFAULTS['logger_name']
    assert all(level == 'debug' for level in log_levels.values())
    assert isinstance(formatter, logging.Formatter)
    assert formatter._fmt == '%(levelname)s:%(message)s'


def test_set_logging_level_normalizes_aliases_and_falls_back_to_default() -> None:
    """Ensure alias levels and invalid values are resolved deterministically."""
    logger = _get_clean_logger()

    log_utils._set_logging_level(logger, 'warn')
    assert logger.level == logging.WARNING

    log_utils._set_logging_level(logger, 'invalid-level')
    assert logger.level == logging.INFO


def test_add_handlers_with_no_output_adds_null_handler() -> None:
    """Ensure _add_handlers uses a null handler when output is disabled."""
    logger = _get_clean_logger()
    formatter = logging.Formatter('%(message)s')

    logger = log_utils._add_handlers(
        _logger=logger,
        _formatter=formatter,
        _no_output=True,
        _file_output=False,
        _file_log_level=None,
        _log_file=None,
        _overwrite_log_files=None,
        _console_output=False,
        _console_log_level=None,
        _syslog_output=False,
        _syslog_log_level=None,
        _syslog_address=None,
        _syslog_port=None,
    )

    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.NullHandler)


def test_add_file_handler_uses_home_directory_for_simple_file_names(tmp_path, monkeypatch) -> None:
    """Ensure bare file names resolve into the user's home directory."""
    logger = _get_clean_logger()
    formatter = logging.Formatter('%(message)s')
    monkeypatch.setattr(log_utils.Path, 'home', lambda: tmp_path)

    logger = log_utils._add_file_handler(
        _logger=logger,
        _log_level='info',
        _log_file='pydplus-test.log',
        _overwrite=True,
        _formatter=formatter,
    )

    file_handler = next(handler for handler in logger.handlers if isinstance(handler, logging.FileHandler))
    assert Path(file_handler.baseFilename) == tmp_path / 'pydplus-test.log'
    assert file_handler.level == logging.INFO
    assert file_handler.mode == 'w'


def test_add_stream_handler_splits_debug_output_between_stdout_and_stderr() -> None:
    """Ensure debug/info console configuration uses split stream handlers."""
    logger = _get_clean_logger()
    formatter = logging.Formatter('%(message)s')

    logger = log_utils._add_stream_handler(logger, 'debug', formatter)
    stdout_handler = next(handler for handler in logger.handlers if getattr(handler, 'stream', None) is sys.stdout)
    stderr_handler = next(handler for handler in logger.handlers if getattr(handler, 'stream', None) is sys.stderr)

    assert len(logger.handlers) == 2
    assert stdout_handler.level == logging.DEBUG
    assert stderr_handler.level == logging.WARNING
    assert any(isinstance(handler_filter, log_utils.LessThanFilter) for handler_filter in stdout_handler.filters)


def test_add_syslog_handler_uses_defaults_when_address_and_port_are_missing(monkeypatch) -> None:
    """Ensure syslog handler falls back to default endpoint values."""
    logger = _get_clean_logger()
    formatter = logging.Formatter('%(message)s')

    class DummySysLogHandler(logging.Handler):
        """Simple SysLog handler stub for testing constructor inputs."""

        def __init__(self, address):
            super().__init__()
            self.address = address

    monkeypatch.setattr(log_utils.logging.handlers, 'SysLogHandler', DummySysLogHandler)
    logger = log_utils._add_syslog_handler(
        _logger=logger,
        _log_level=None,
        _formatter=formatter,
        _address=None,
        _port=None,
    )

    assert len(logger.handlers) == 1
    syslog_handler = logger.handlers[0]
    assert isinstance(syslog_handler, DummySysLogHandler)
    assert syslog_handler.address == (
        log_utils.HANDLER_DEFAULTS['syslog_address'],
        log_utils.HANDLER_DEFAULTS['syslog_port'],
    )
    assert syslog_handler.level == logging.INFO


def test_less_than_filter_only_allows_records_below_the_maximum_level() -> None:
    """Ensure LessThanFilter blocks records with levels at or above the threshold."""
    level_filter = log_utils.LessThanFilter(logging.WARNING)
    info_record = logging.LogRecord('test', logging.INFO, __file__, 1, 'msg', (), None)
    warning_record = logging.LogRecord('test', logging.WARNING, __file__, 2, 'msg', (), None)

    assert level_filter.filter(info_record) is True
    assert level_filter.filter(warning_record) is False
