# -*- coding: utf-8 -*-
"""
:Module:            dev.dev_logging
:Synopsis:          Helper module that enables debug logging for development of the PyDPlus package
:Usage:             ``from dev.dev_logging import setup_dev_logging``
:Example:           ``logger = setup_dev_logging('pydplus.console')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     30 Mar 2026
"""

from __future__ import annotations

import logging
from typing import Optional

from pydplus.utils import log_utils


def setup_dev_logging(
    logger_name: str,
    *,
    debug: bool = True,
    console: bool = True,
    file: bool = False,
    log_file: Optional[str] = None,
    overwrite: bool = True,
    configure_root: bool = True,
):
    """Initialize a development-friendly logger using pydplus.log_utils.

    :param logger_name: Typically uses ``__name__`` from the calling module
    :param debug: Enable debug-level logging across all handlers
    :param console: Enable console (stdout/stderr) logging
    :param file: Enable file logging
    :param log_file: Optional file path (defaults to ./pydplus-dev.log if file=True)
    :param overwrite: Overwrite log file on each run
    :param configure_root: Configure the root logger so package-wide module logs are visible
    :returns: The configured logger instance
    """
    if file and not log_file:
        log_file = './pydplus-dev.log'

    target_logger_name = 'root' if configure_root else logger_name
    log_utils.initialize_logging(
        logger_name=target_logger_name,
        debug=debug,
        console_output=console,
        file_output=file,
        log_file=log_file,
        overwrite_log_files=overwrite,
    )
    logger = logging.getLogger(logger_name)

    logger.debug('Development logging initialized')
    logger.debug(
        'Logging config | debug=%s console=%s file=%s log_file=%s configure_root=%s',
        debug,
        console,
        file,
        log_file,
        configure_root,
    )

    return logger
