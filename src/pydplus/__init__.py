# -*- coding: utf-8 -*-
"""
:Module:            pydplus
:Synopsis:          This is the ``__init__`` module for the pydplus package
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     19 May 2025
"""

from . import core
from .core import PyDPlus
from .utils import version

__all__ = ['core', 'PyDPlus']

# Define the package version by pulling from the pydplus.utils.version module
__version__ = version.get_full_version()
