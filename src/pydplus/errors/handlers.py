# -*- coding: utf-8 -*-
"""
:Module:            pydplus.errors.handlers
:Synopsis:          Functions that handle various error situations within the namespace
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     07 Mar 2026
"""

from __future__ import annotations

import warnings
from typing import Type

from .. import constants as const


def get_exception_type(exc) -> str:
    """Return the exception type (e.g. ``RuntimeError``, ``TypeError``, etc.) for a given exception.

    :returns: The exception type as a string
    """
    return type(exc).__name__


def display_warning(
    message: str,
    *,
    category: Type[Warning] = const._DEFAULT_WARNING_CATEGORY,
    stacklevel: int = 2,
) -> None:
    """Emit a warning that points to the caller by default.

    :param message: Warning message to emit
    :type message: str
    :param category: Warning category class (default: ``UserWarning``)
    :type category: type[Warning]
    :param stacklevel: How far up the call stack to attribute the warning (``2`` by default - caller of this helper)
    :type stacklevel: int
    :returns: None
    """
    warnings.warn(message, category=category, stacklevel=stacklevel)
