# -*- coding: utf-8 -*-
"""
:Module:         pydplus.tests.test_instantiate_object
:Synopsis:       This module is used by pytest to test instantiating the core object
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  10 Jun 2025
"""

import pytest

from . import resources
from .. import errors


def test_instantiate_empty_core_object():
    """This function tests the ability to instantiate an empty core object.

    .. versionadded:: 1.0.0
    """
    # Check to ensure the MissingRequiredDataError exception is raised due to missing base_url value
    with pytest.raises(errors.exceptions.MissingRequiredDataError):
        # Instantiate the core object without any parameters
        resources.get_core_object(init_method='param')
