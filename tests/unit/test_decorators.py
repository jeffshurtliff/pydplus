# -*- coding: utf-8 -*-
"""
:Module:            tests.unit.test_decorators
:Synopsis:          Unit tests for pydplus decorators
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff (via GPT-5.3-codex)
:Modified Date:     30 Mar 2026
"""

from __future__ import annotations

import warnings
from pathlib import Path

import pytest

from pydplus import decorators

pytestmark = pytest.mark.unit


def test_deprecated_emits_default_warning_and_preserves_callable_behavior() -> None:
    """Ensure deprecated emits a default warning and returns the wrapped result."""

    @decorators.deprecated(since='1.0.0')
    def legacy_add(x: int, y: int) -> int:
        return x + y

    with warnings.catch_warnings(record=True) as warning_records:
        warnings.simplefilter('always')
        result = legacy_add(2, 3)

    assert result == 5
    assert len(warning_records) == 1
    assert warning_records[0].category is DeprecationWarning
    assert str(warning_records[0].message) == 'legacy_add is deprecated since 1.0.0.'


def test_deprecated_message_includes_replacement_and_removal_details() -> None:
    """Ensure optional replacement and removal values are included in the warning message."""

    @decorators.deprecated(since='1.2.0', replacement='new_function()', removal='2.0.0')
    def old_function() -> str:
        return 'ok'

    with warnings.catch_warnings(record=True) as warning_records:
        warnings.simplefilter('always')
        result = old_function()

    assert result == 'ok'
    assert len(warning_records) == 1
    assert str(warning_records[0].message) == (
        'old_function is deprecated since 1.2.0. Use new_function() instead. It will be removed in 2.0.0.'
    )


def test_deprecated_preserves_wrapped_function_metadata() -> None:
    """Ensure functools.wraps preserves expected metadata on wrapped callables."""

    @decorators.deprecated(since='1.1.0')
    def legacy_value() -> str:
        """A legacy function docstring."""
        return 'legacy'

    assert legacy_value.__name__ == 'legacy_value'
    assert legacy_value.__doc__ == 'A legacy function docstring.'
    assert hasattr(legacy_value, '__wrapped__')


def test_deprecated_supports_custom_warning_category_and_stacklevel() -> None:
    """Ensure category and stacklevel values are forwarded to warnings.warn."""

    @decorators.deprecated(since='1.0.0', category=UserWarning, stacklevel=1)
    def stacklevel_one() -> None:
        return None

    @decorators.deprecated(since='1.0.0', category=UserWarning, stacklevel=2)
    def stacklevel_two() -> None:
        return None

    with warnings.catch_warnings(record=True) as warning_records:
        warnings.simplefilter('always')
        stacklevel_one()
        stacklevel_two()

    assert len(warning_records) == 2
    assert warning_records[0].category is UserWarning
    assert warning_records[1].category is UserWarning
    assert Path(warning_records[0].filename).name == 'decorators.py'
    assert Path(warning_records[1].filename).name == 'test_decorators.py'
