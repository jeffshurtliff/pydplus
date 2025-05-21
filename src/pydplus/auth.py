# -*- coding: utf-8 -*-
"""
:Module:            pydplus.auth
:Synopsis:          This module performs the authentication and authorization operations
:Usage:             ``from pydplus import auth``
:Example:           TBD
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     21 May 2025
"""

from . import errors

# Define constants
DEFAULT_CONNECTION_TYPE = 'oauth'
VALID_CONNECTION_TYPES = {'oauth', 'legacy'}
LEGACY_CONNECTION_FIELDS = {'access_id', 'private_key_path', 'private_key_file'}
OAUTH_CONNECTION_FIELDS = {'issuer_url', 'client_id', 'grant_type', 'client_authentication'}
OAUTH_GRANT_TYPE = 'Client Credentials'
OAUTH_CLIENT_AUTH = 'Private Key JWT'
