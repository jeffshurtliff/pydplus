# -*- coding: utf-8 -*-
"""
:Module:            pydplus.utils.log_utils
:Synopsis:          Collection of logging utilities and functions
:Usage:             ``from pydplus.utils import log_utils``
:Example:           ``logger = log_utils.initialize_logging(__name__)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff (via GPT-5.3-codex)
:Modified Date:     16 Mar 2026
"""

from __future__ import annotations

import logging
import logging.handlers
import sys
from pathlib import Path
from types import MappingProxyType
from typing import Dict, Mapping, Optional, Tuple, Union


LOGGING_DEFAULTS: Mapping[str, str] = MappingProxyType({
    'logger_name': __name__,
    'log_level': 'info',
    'format': '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    'date_format': '%Y-%m-%d %I:%M:%S',
})
HANDLER_DEFAULTS: Mapping[str, Union[str, int]] = MappingProxyType({
    'file_log_level': 'info',
    'console_log_level': 'warning',
    'syslog_log_level': 'info',
    'syslog_address': 'localhost',
    'syslog_port': 514,
})
LOG_LEVELS: Mapping[str, int] = MappingProxyType({
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
})
MANAGED_HANDLER_ATTR = '_pydplus_managed_handler'


def initialize_logging(
        logger_name: Optional[str] = None,
        log_level: Optional[Union[str, int]] = None,
        formatter: Optional[Union[str, logging.Formatter]] = None,
        debug: Optional[bool] = None,
        no_output: Optional[bool] = None,
        file_output: Optional[bool] = None,
        file_log_level: Optional[Union[str, int]] = None,
        log_file: Optional[str] = None,
        overwrite_log_files: Optional[bool] = None,
        console_output: Optional[bool] = None,
        console_log_level: Optional[Union[str, int]] = None,
        syslog_output: Optional[bool] = None,
        syslog_log_level: Optional[Union[str, int]] = None,
        syslog_address: Optional[str] = None,
        syslog_port: Optional[int] = None,
) -> logging.Logger:
    """Initialize and configure a logger instance.

    :param logger_name: The logger name used by :py:func:`logging.getLogger`.
    :param log_level: The overall logger level.
    :param formatter: Optional formatter instance or format string.
    :param debug: If ``True``, force all logger and handler levels to ``debug``.
    :param no_output: If ``True``, add a :py:class:`logging.NullHandler` and skip all output handlers.
    :param file_output: If ``True``, enable file-based logging output.
    :param file_log_level: Log level for the file handler.
    :param log_file: Log file name or path for file output.
    :param overwrite_log_files: If ``True``, overwrite the log file instead of appending.
    :param console_output: If ``True``, enable console logging output.
    :param console_log_level: Log level for console output.
    :param syslog_output: If ``True``, enable syslog output.
    :param syslog_log_level: Log level for syslog output.
    :param syslog_address: Hostname or IP address for the syslog endpoint.
    :param syslog_port: Port for the syslog endpoint.
    :returns: A configured :py:class:`logging.Logger` instance.
    """
    logger_name, log_levels, formatter = _apply_defaults(logger_name, formatter, debug, log_level, file_log_level,
                                                         console_log_level, syslog_log_level)
    log_level, file_log_level, console_log_level, syslog_log_level = _get_log_levels_from_dict(log_levels)
    logger = logging.getLogger(logger_name)
    logger = _set_logging_level(logger, log_level)
    _remove_managed_handlers(logger)
    logger = _add_handlers(logger, formatter, no_output, file_output, file_log_level, log_file, overwrite_log_files,
                           console_output, console_log_level, syslog_output, syslog_log_level, syslog_address,
                           syslog_port)
    return logger


class LessThanFilter(logging.Filter):
    """Allow filters to be set to limit log levels to only less than a specified level.

    .. seealso:: `Zoey Greer <https://stackoverflow.com/users/5124424/zoey-greer>`_ is the original author of
                 this class which was provided on `Stack Overflow <https://stackoverflow.com/a/31459386>`_.
    """
    def __init__(self, exclusive_maximum: int, name: str = '') -> None:
        """Instantiate a filter with an exclusive maximum log level.

        :param exclusive_maximum: The maximum log level (exclusive) to allow.
        :param name: Optional logger name for inherited :py:class:`logging.Filter` behavior.
        """
        super().__init__(name)
        self.max_level = exclusive_maximum

    def filter(self, record: logging.LogRecord) -> bool:
        """Return whether a message should be logged.

        .. note:: A truthy return indicates that the message will be logged.
        """
        return record.levelno < self.max_level


def _apply_defaults(
        _logger_name: Optional[str],
        _formatter: Optional[Union[str, logging.Formatter]],
        _debug: Optional[bool],
        _log_level: Optional[Union[str, int]],
        _file_level: Optional[Union[str, int]],
        _console_level: Optional[Union[str, int]],
        _syslog_level: Optional[Union[str, int]],
) -> Tuple[str, Dict[str, str], logging.Formatter]:
    """Apply default values to the configuration settings if not explicitly defined.

    :param _logger_name: The name of the logger instance
    :param _formatter: The log format to utilize for the logger instance
    :param _debug: Defines if debug mode is enabled
    :param _log_level: The general logging level for the logger instance
    :returns: The values that will be used for the configuration settings
    """
    _default_log_level = LOGGING_DEFAULTS.get('log_level', 'info')
    _log_levels = {
        'general': _normalize_log_level(_log_level, _default_log_level),
        'file': _file_level,
        'console': _console_level,
        'syslog': _syslog_level,
    }
    _logger_name = LOGGING_DEFAULTS.get('logger_name', __name__) if not _logger_name else _logger_name
    if _debug:
        for _log_type in _log_levels:
            _log_levels[_log_type] = 'debug'
    else:
        for _lvl_type, _lvl_value in _log_levels.items():
            if _lvl_value is None:
                _log_levels[_lvl_type] = _log_levels['general']
            else:
                _log_levels[_lvl_type] = _normalize_log_level(_lvl_value, _log_levels['general'])
    _formatter = _resolve_formatter(_formatter)
    return _logger_name, _log_levels, _formatter


def _get_log_levels_from_dict(_log_levels: Mapping[str, str]) -> Tuple[str, str, str, str]:
    """Return the individual log level values from a dictionary.

    :param _log_levels: Dictionary containing log levels for different handlers
    :returns: Individual string values for each handler
    """
    _general = _log_levels.get('general', str(HANDLER_DEFAULTS.get('file_log_level', 'info')))
    _file = _log_levels.get('file', _general)
    _console = _log_levels.get('console', _general)
    _syslog = _log_levels.get('syslog', _general)
    return _general, _file, _console, _syslog


def _set_logging_level(_logger: Union[logging.Logger, logging.Handler], _log_level: Optional[Union[str, int]]
                       ) -> Union[logging.Logger, logging.Handler]:
    """Set the logging level for a :py:class:`logging.Logger` instance.

    :param _logger: The :py:class:`logging.Logger` or :py:class:`logging.Handler` instance
    :param _log_level: The log level as a string (``debug``, ``info``, ``warning``, ``error`` or ``critical``)
    :returns: The :py:class:`logging.Logger` instance with a logging level set where applicable
    """
    _normalized_level = _normalize_log_level(_log_level, LOGGING_DEFAULTS.get('log_level', 'info'))
    _logger.setLevel(LOG_LEVELS[_normalized_level])
    return _logger


def _add_handlers(
        _logger: logging.Logger,
        _formatter: logging.Formatter,
        _no_output: Optional[bool],
        _file_output: Optional[bool],
        _file_log_level: Optional[str],
        _log_file: Optional[str],
        _overwrite_log_files: Optional[bool],
        _console_output: Optional[bool],
        _console_log_level: Optional[str],
        _syslog_output: Optional[bool],
        _syslog_log_level: Optional[str],
        _syslog_address: Optional[str],
        _syslog_port: Optional[int],
) -> logging.Logger:
    """Add output handlers to a logger instance.

    :param _logger: The logger instance to configure.
    :param _formatter: Formatter applied to emitted log records.
    :param _no_output: Whether to suppress all output handlers and use a null handler.
    :param _file_output: Whether to add a file handler.
    :param _file_log_level: The file handler log level.
    :param _log_file: The output file path or file name.
    :param _overwrite_log_files: Whether to overwrite instead of append.
    :param _console_output: Whether to add console output handlers.
    :param _console_log_level: The console handler log level.
    :param _syslog_output: Whether to add a syslog handler.
    :param _syslog_log_level: The syslog handler log level.
    :param _syslog_address: The syslog hostname/address.
    :param _syslog_port: The syslog port.
    :returns: The logger instance with configured handlers.
    """
    if _no_output or not any((_file_output, _console_output, _syslog_output)):
        _logger.addHandler(_mark_handler_as_managed(logging.NullHandler()))
    else:
        if _file_output:
            # Add the FileHandler to the Logger object
            _logger = _add_file_handler(_logger, _file_log_level, _log_file, _overwrite_log_files, _formatter)
        if _console_output:
            # Add the StreamHandler to the Logger object
            _logger = _add_stream_handler(_logger, _console_log_level, _formatter)
        if _syslog_output:
            # Add the SyslogHandler to the Logger object
            _logger = _add_syslog_handler(_logger, _syslog_log_level, _formatter, _syslog_address, _syslog_port)
    return _logger


def _add_file_handler(
        _logger: logging.Logger,
        _log_level: Optional[str],
        _log_file: Optional[str],
        _overwrite: Optional[bool],
        _formatter: logging.Formatter,
) -> logging.Logger:
    """Add a :py:class:`logging.FileHandler` to the :py:class:`logging.Logger` instance.

    :param _logger: The :py:class:`logging.Logger` instance
    :param _log_level: The log level to set for the handler
    :param _log_file: The log file (as a file name or a file path) to which messages should be written

    .. note:: If a file path isn't provided then the default directory is the home directory of the user instantiating
              the :py:class:`logging.Logger` object. If a file name is also no provided then it will default to
              using ``pydplus.log`` as the file name.

    :param _overwrite: Determines if messages should be appended to the file (default) or overwrite it
    :param _formatter: The :py:class:`logging.Formatter` to apply to messages passed through the handler
    :returns: The :py:class:`logging.Logger` instance with the added :py:class:`logging.FileHandler`
    """
    # Define the log file to use
    _home_dir = Path.home()
    if _log_file:
        _path = Path(_log_file).expanduser()
        if _path.parent == Path('.'):
            _path = _home_dir / _path
    else:
        _path = _home_dir / 'pydplus.log'

    _path.parent.mkdir(parents=True, exist_ok=True)

    # Identify if log file should be overwritten
    _write_mode = 'w' if _overwrite else 'a'

    # Instantiate the handler
    _handler = logging.FileHandler(_path, _write_mode, encoding='utf-8')
    _log_level = _normalize_log_level(_log_level, str(HANDLER_DEFAULTS.get('file_log_level', 'info')))
    _handler = _set_logging_level(_handler, _log_level)
    _handler.setFormatter(_formatter)

    # Add the handler to the logger
    _logger.addHandler(_mark_handler_as_managed(_handler))
    return _logger


def _add_stream_handler(_logger: logging.Logger, _log_level: Optional[str], _formatter: logging.Formatter) -> logging.Logger:
    """Add a :py:class:`logging.StreamHandler` to the :py:class:`logging.Logger` instance.

    :param _logger: The :py:class:`logging.Logger` instance
    :param _log_level: The log level to set for the handler
    :param _formatter: The :py:class:`logging.Formatter` to apply to messages passed through the handler
    :returns: The :py:class:`logging.Logger` instance with the added :py:class:`logging.StreamHandler`
    """
    _log_level = _normalize_log_level(_log_level, str(HANDLER_DEFAULTS.get('console_log_level', 'warning')))
    _stdout_levels = ('debug', 'info')
    if _log_level in _stdout_levels:
        _logger = _add_split_stream_handlers(_logger, _log_level, _formatter)
    else:
        _handler = logging.StreamHandler()
        _handler = _set_logging_level(_handler, _log_level)
        _handler.setFormatter(_formatter)
        _logger.addHandler(_mark_handler_as_managed(_handler))
    return _logger


def _add_split_stream_handlers(_logger: logging.Logger, _log_level: str, _formatter: logging.Formatter) -> logging.Logger:
    """Split messages into ``stdout`` or ``stderr`` handlers depending on the log level.

    .. seealso:: Refer to the documentation for the :py:class:`pydplus.utils.log_utils.LessThanFilter` for
                 more information on how this filtering is implemented and for credit to the original author.

    :param _logger: The :py:class:`logging.Logger` instance
    :param _log_level: The log level provided for the stream handler (i.e. console output)
    :param _formatter: The :py:class:`logging.Formatter` to apply to messages passed through the handlers
    :returns: The logger instance with the two handlers added
    """
    # Configure and add the STDOUT handler
    _stdout_handler = logging.StreamHandler(sys.stdout)
    _stdout_handler = _set_logging_level(_stdout_handler, _log_level)
    _stdout_handler.addFilter(LessThanFilter(logging.WARNING))
    _stdout_handler.setFormatter(_formatter)
    _logger.addHandler(_mark_handler_as_managed(_stdout_handler))

    # Configure and add the STDERR handler
    _stderr_handler = logging.StreamHandler(sys.stderr)
    _stderr_handler.setLevel(logging.WARNING)
    _stderr_handler.setFormatter(_formatter)
    _logger.addHandler(_mark_handler_as_managed(_stderr_handler))

    # Return the logger with the added handlers
    return _logger


def _add_syslog_handler(
        _logger: logging.Logger,
        _log_level: Optional[str],
        _formatter: logging.Formatter,
        _address: Optional[str],
        _port: Optional[int],
) -> logging.Logger:
    """Add a :py:class:`logging.handlers.SysLogHandler` to the logger instance.

    :param _logger: The logger to which the handler should be added.
    :param _log_level: The log level to apply to the syslog handler.
    :param _formatter: The formatter applied to syslog messages.
    :param _address: The syslog server address.
    :param _port: The syslog server port.
    :returns: The logger instance with the configured syslog handler.
    """
    _log_level = _normalize_log_level(_log_level, str(HANDLER_DEFAULTS.get('syslog_log_level', 'info')))
    _address = str(HANDLER_DEFAULTS.get('syslog_address', 'localhost')) if not _address else _address
    _port = int(HANDLER_DEFAULTS.get('syslog_port', 514)) if _port is None else _port
    _handler = logging.handlers.SysLogHandler(address=(_address, _port))
    _handler = _set_logging_level(_handler, _log_level)
    _handler.setFormatter(_formatter)
    _logger.addHandler(_mark_handler_as_managed(_handler))
    return _logger


def _resolve_formatter(_formatter: Optional[Union[str, logging.Formatter]]) -> logging.Formatter:
    """Return a :py:class:`logging.Formatter` instance from supported formatter input values.

    :param _formatter: The formatter object or format string.
    :returns: A formatter instance ready for handler usage.
    """
    if isinstance(_formatter, logging.Formatter):
        return _formatter
    if isinstance(_formatter, str):
        return logging.Formatter(_formatter, datefmt=LOGGING_DEFAULTS.get('date_format'))
    return logging.Formatter(LOGGING_DEFAULTS.get('format'), datefmt=LOGGING_DEFAULTS.get('date_format'))


def _normalize_log_level(_log_level: Optional[Union[str, int]], _fallback: str) -> str:
    """Normalize a log level value to one of the accepted level-name strings.

    :param _log_level: The supplied log level as a string or integer.
    :param _fallback: The fallback log level to use for invalid or missing input.
    :returns: A normalized log level string (``debug``, ``info``, ``warning``, ``error``, ``critical``).
    """
    if isinstance(_log_level, int):
        _name = logging.getLevelName(_log_level)
        if isinstance(_name, str) and _name.lower() in LOG_LEVELS:
            return _name.lower()
        return _fallback

    if isinstance(_log_level, str):
        _normalized = _log_level.strip().lower()
        _normalized = 'warning' if _normalized == 'warn' else _normalized
        _normalized = 'critical' if _normalized == 'fatal' else _normalized
        if _normalized in LOG_LEVELS:
            return _normalized
    return _fallback


def _mark_handler_as_managed(_handler: logging.Handler) -> logging.Handler:
    """Mark a handler as managed by this module.

    :param _handler: The handler instance to mark.
    :returns: The marked handler instance.
    """
    setattr(_handler, MANAGED_HANDLER_ATTR, True)
    return _handler


def _remove_managed_handlers(_logger: logging.Logger) -> None:
    """Remove any handlers managed by this module from the logger.

    :param _logger: The logger instance to clean up.
    """
    for _handler in list(_logger.handlers):
        if getattr(_handler, MANAGED_HANDLER_ATTR, False):
            _logger.removeHandler(_handler)
            _handler.close()
