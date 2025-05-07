# -*- coding: utf-8 -*-
"""
:Module:            pydplus.errors.handlers
:Synopsis:          Functions that handle various error situations within the namespace
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     06 May 2025
"""

import sys


def eprint(*args, **kwargs):
    """This function behaves the same as the ``print()`` function but is leveraged to print errors to ``sys.stderr``.

    .. versionadded:: 1.0.0
    """
    print(*args, file=sys.stderr, **kwargs)
