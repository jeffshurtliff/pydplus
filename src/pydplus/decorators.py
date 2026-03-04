# -*- coding: utf-8 -*-
"""
:Module:            pydplus.decorators
:Synopsis:          Decorators that can be used to include additional functionality with functions and methods
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     04 Mar 2026
"""

from __future__ import annotations

import functools
import warnings
from typing import Any, Callable, Optional, Type, TypeVar

# Define the function Type bound to Callable
F = TypeVar("F", bound=Callable[..., Any])


def deprecated(
    *,
    since: str,
    replacement: Optional[str] = None,
    removal: Optional[str] = None,
    category: Type[Warning] = DeprecationWarning,
    stacklevel: int = 2,
) -> Callable[[F], F]:
    """Marks a callable as deprecated and emits a warning at runtime.

    :param since: Version when deprecation started
    :type since: str
    :param replacement: Suggested replacement usage (string)
    :type replacement: str, None
    :param removal: Version when it will be removed (optional)
    :type removal: str, None
    :param category: Warning category (default: :py:exc:`DeprecationWarning`)
    :type category: type[Warning]
    :param stacklevel: Warning stacklevel (default: ``2``)
    :type stacklevel: int
    """
    def decorator(func: F) -> F:
        message_parts = [f"{func.__name__} is deprecated since {since}."]
        if replacement:
            message_parts.append(f"Use {replacement} instead.")
        if removal:
            message_parts.append(f"It will be removed in {removal}.")
        message = " ".join(message_parts)

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            warnings.warn(message, category=category, stacklevel=stacklevel)
            return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator
