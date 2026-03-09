# -*- coding: utf-8 -*-
"""
:Module:            tests.unit.test_error_handlers
:Synopsis:          Unit tests for pydplus error handler utilities
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff (via GPT-5.3-codex)
:Modified Date:     09 Mar 2026
"""

from __future__ import annotations

import pytest

from pydplus.errors import handlers


pytestmark = pytest.mark.unit


def test_get_exception_type_returns_class_name() -> None:
    """Ensure the helper returns the concrete exception class name."""
    assert handlers.get_exception_type(ValueError('invalid')) == 'ValueError'


def test_display_warning_emits_warning() -> None:
    """Ensure warning helper emits a warning with the provided message."""
    with pytest.warns(UserWarning, match='test warning'):
        handlers.display_warning('test warning')
