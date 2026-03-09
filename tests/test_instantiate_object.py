# -*- coding: utf-8 -*-
"""
:Module:         pydplus.tests.test_instantiate_object
:Synopsis:       This module is used by pytest to test instantiating the core client object
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  09 Mar 2026
"""

from __future__ import annotations

import pytest

from . import resources
from pydplus import errors


def test_instantiate_empty_core_object():
    """Test the ability to instantiate an empty core client object."""
    # Check to ensure the MissingRequiredDataError exception is raised due to missing base_url value
    with pytest.raises(errors.exceptions.MissingRequiredDataError):
        # Instantiate the core object without any parameters
        resources.get_core_object(init_method='param')
