###################
PyDPlus Core Object
###################
This section provides details around the core module and the methods used
within the core object for the **pydplus** package, which are listed below.

* `Init Module (pydplus)`_
* `Core Module (pydplus.core)`_
    * `Core Functionality Subclasses (pydplus.core.PyDPlus)`_
        * `User Subclass (pydplus.core.PyDPlus.User)`_

|

**************************
Init Module (pydplus)
**************************
This module (being the primary ``__init__.py`` file for the library) provides a
"jumping-off-point" to initialize the primary :py:class:`pydplus.core.PyDPlus` object.

.. automodule:: pydplus
   :members: PyDPlus
   :special-members: __init__

:doc:`Return to Top <core-object-methods>`

|

**************************
Core Module (pydplus.core)
**************************
This module contains the core object and functions to establish the connection to the
tenant and leverage it to perform various actions.

.. automodule:: pydplus.core
   :members:
   :special-members: __init__

:doc:`Return to Top <core-object-methods>`

|

Core Functionality Subclasses (pydplus.core.PyDPlus)
====================================================
These classes below are inner/nested classes within the core :py:class:`pydplus.core.PyDPlus` class.

.. note:: The classes themselves are *PascalCase* format and singular (e.g. ``User``, etc.) whereas
          the names used to call the inner class methods are all *lowercase* (or *snake_case*) and plural.
          (e.g. ``core_object.user.get_user_details()``, etc.)

|

User Subclass (pydplus.core.PyDPlus.User)
-----------------------------------------
.. autoclass:: pydplus.core::PyDPlus.User
   :members:
   :noindex:

:doc:`Return to Top <core-object-methods>`

|
