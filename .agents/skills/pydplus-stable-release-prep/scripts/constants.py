# -*- coding: utf-8 -*-
"""
:Module:            pydplus_stable_release_constants
:Synopsis:          Defines constants for the standalone PyDPlus release artifact inspector
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff (via GPT-6)
:Modified Date:     12 Sep 2026
"""

import re
from pathlib import Path

EXPECTED_PROJECT_NAME: str = 'pydplus'
DEFAULT_PROJECT_ROOT: Path = Path(__file__).resolve().parents[4]
NORMALIZE_NAME: re.Pattern[str] = re.compile(r'[-_.]+')
FORBIDDEN_COMPONENTS: set[str] = {
    '.env',
    '.envrc',
    '.git',
    '.pytest_cache',
    '.ruff_cache',
    '__pycache__',
    'local',
    'secrets',
}
FORBIDDEN_BASENAMES: set[str] = {
    '.ds_store',
    '.netrc',
    '.pypirc',
    'credentials.json',
    'credentials.yaml',
    'credentials.yml',
    'id_ed25519',
    'id_rsa',
    'private-key.pem',
    'private_key.pem',
    'service-account.json',
    'token.json',
}
ALLOWED_DIST_METADATA: set[str] = {'SHA256SUMS'}
