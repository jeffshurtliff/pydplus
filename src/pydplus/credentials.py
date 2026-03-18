# -*- coding: utf-8 -*-
"""
:Module:            pydplus.credentials
:Synopsis:          Secure parsing and handling for RSA ID Plus legacy key material
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     18 Mar 2026
"""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Optional, Union, cast
from urllib.parse import urlparse

from . import constants as const
from .utils import log_utils
from .errors.exceptions import IDPlusCredentialError

# Initialize logging
logger = log_utils.initialize_logging(__name__)

# Define the _slots_dataclass property based on the python version
if sys.version_info >= (3, 10):
    _slots_dataclass = cast(Any, dataclass)(slots=True)
else:
    _slots_dataclass = dataclass


@_slots_dataclass
class IDPlusLegacyKeyMaterial:
    """Typed RSA ID Plus legacy credential material parsed from a `.key` JSON file.

    :param customer_name: The RSA tenant customer name from the key file
    :type customer_name: str
    :param access_id: The legacy API access identifier
    :type access_id: str
    :param access_key_pem: The RSA private key in PEM format
    :type access_key_pem: str
    :param admin_rest_api_url: The Admin REST API base URL for the tenant
    :type admin_rest_api_url: str
    :param description: Optional free-form description from the key file
    :type description: str, None
    :raises: :py:exc:`pydplus.errors.exceptions.IDPlusCredentialError`
    """
    # Define the class variables
    customer_name: str
    access_id: str
    access_key_pem: str = field(repr=False)
    admin_rest_api_url: str
    description: Optional[str] = None

    @classmethod
    def from_json_text(cls, text: str) -> IDPlusLegacyKeyMaterial:
        """Parse key material from JSON text and validate the resulting object.

        :param text: JSON content for the RSA ID Plus `.key` file
        :type text: str
        :returns: Parsed and validated key material
        :raises :py:exc:`TypeError`,
                :py:exc:`pydplus.errors.exceptions.IDPlusCredentialError`
        """
        if not isinstance(text, str):
            exc_msg = f"The 'text' parameter must be a string (Provided: {type(text)})"
            logger.error(exc_msg)
            raise TypeError(exc_msg)

        try:
            payload = json.loads(text)
        except json.JSONDecodeError as exc:
            exc_msg = 'The provided key material is not valid JSON'
            logger.error(exc_msg)
            raise IDPlusCredentialError(exc_msg) from exc

        if not isinstance(payload, dict):
            exc_msg = 'The provided key material JSON must be an object at the root level'
            logger.error(exc_msg)
            raise IDPlusCredentialError(exc_msg)

        key_material = cls(
            customer_name=_extract_required_string(
                payload,
                const.CREDENTIAL_VALUES.JSON_FIELD_CUSTOMER_NAME,
            ),
            access_id=_extract_required_string(
                payload,
                const.CREDENTIAL_VALUES.JSON_FIELD_ACCESS_ID,
            ),
            access_key_pem=_extract_required_string(
                payload,
                const.CREDENTIAL_VALUES.JSON_FIELD_ACCESS_KEY,
            ),
            admin_rest_api_url=_extract_required_string(
                payload,
                const.CREDENTIAL_VALUES.JSON_FIELD_ADMIN_REST_API_URL,
            ),
            description=_extract_optional_string(
                payload,
                const.CREDENTIAL_VALUES.JSON_FIELD_DESCRIPTION,
            ),
        )
        key_material.validate()
        return key_material

    @classmethod
    def from_file(cls, path: Union[str, Path]) -> IDPlusLegacyKeyMaterial:
        """Parse key material from a `.key` file path and validate the result.

        :param path: The path to the `.key` JSON file
        :returns: Parsed and validated key material
        :raises :py:exc:`TypeError`,
                :py:exc:`pydplus.errors.exceptions.IDPlusCredentialError`
        """
        if not isinstance(path, (str, Path)):
            exc_msg = f"The 'path' parameter must be a string or Path object (Provided: {type(path)})"
            logger.error(exc_msg)
            raise TypeError(exc_msg)

        key_path = Path(path).expanduser()
        try:
            key_text = key_path.read_text(encoding='utf-8')
        except OSError as exc:
            exc_msg = f"Unable to read key material from '{key_path}'"
            logger.error(exc_msg)
            raise IDPlusCredentialError(exc_msg) from exc

        return cls.from_json_text(key_text)

    def validate(self) -> None:
        """Validate the key material fields and URL/private-key requirements.

        :raises :py:exc:`pydplus.errors.exceptions.IDPlusCredentialError`
        """
        if not self.customer_name.strip():
            exc_msg = 'The customer name cannot be empty'
            logger.error(exc_msg)
            raise IDPlusCredentialError(exc_msg)

        if not self.access_id.strip():
            exc_msg = 'The access ID cannot be empty'
            logger.error(exc_msg)
            raise IDPlusCredentialError(exc_msg)

        if not self.access_key_pem.strip():
            exc_msg = 'The access key cannot be empty'
            logger.error(exc_msg)
            raise IDPlusCredentialError(exc_msg)

        if const.CREDENTIAL_VALUES.PEM_BEGIN_MARKER not in self.access_key_pem:
            exc_msg = 'The access key does not appear to be a valid RSA private key PEM value'
            logger.error(exc_msg)
            raise IDPlusCredentialError(exc_msg)

        parsed_url = urlparse(self.admin_rest_api_url)
        if parsed_url.scheme.lower() != const.URLS.HTTPS_SCHEME or not parsed_url.netloc:
            exc_msg = 'The admin REST API URL must be a valid HTTPS URL'
            logger.error(exc_msg)
            raise IDPlusCredentialError(exc_msg)

        if not parsed_url.hostname:
            exc_msg = 'The admin REST API URL must include a valid host value'
            logger.error(exc_msg)
            raise IDPlusCredentialError(exc_msg)

        if self.description is not None and not isinstance(self.description, str):
            exc_msg = 'The optional description must be a string when provided'
            logger.error(exc_msg)
            raise IDPlusCredentialError(exc_msg)

    @property
    def tenant_host(self) -> str:
        """The host component parsed from :attr:`admin_rest_api_url`."""
        return urlparse(self.admin_rest_api_url).hostname or ''

    @property
    def default_pem_filename(self) -> str:
        """Return a sanitized default filename for persisted private key material."""
        customer_slug = _slugify(self.customer_name)
        access_id_slug = _slugify(self.access_id)

        if not customer_slug:
            customer_slug = const.CREDENTIAL_VALUES.DEFAULT_FILENAME_FALLBACK

        if access_id_slug:
            safe_name = f'{customer_slug}-{access_id_slug}'
        else:
            safe_name = customer_slug

        return f"{safe_name}{const.CREDENTIAL_VALUES.DEFAULT_PEM_EXTENSION}"

    def private_key_bytes(self) -> bytes:
        """Return the private key as UTF-8 encoded bytes."""
        return self.access_key_pem.encode(const.UTF8_ENCODING)

    @staticmethod
    def _default_cert_dir() -> Path:
        """Return the default directory for secure private-key persistence."""
        return (
            Path.home()
            / const.CREDENTIAL_VALUES.DEFAULT_CERT_HOME_DIR
            / const.CREDENTIAL_VALUES.DEFAULT_CERT_SUBDIR
        )

    def write_private_key_pem(
        self,
        path: Optional[Union[str, Path]] = None,
        overwrite: bool = False,
    ) -> Path:
        """Persist private key material to disk with strict file-system protections.

        .. note::
           Persistence is explicit-only and never occurs automatically during parsing.

        :param path: Optional destination path (Defaults to ``~/.pydplus/certs/<safe_filename>.pem``)
        :param overwrite: Whether to overwrite an existing destination file (``False`` by default)
        :returns: The final path for the persisted PEM file
        :raises :py:exc:`FileExistsError`,
                :py:exc:`pydplus.errors.exceptions.IDPlusCredentialError`
        """
        self.validate()

        if path is None:
            cert_dir = self._default_cert_dir()
            _ensure_private_dir(cert_dir, enforce_mode=True)
            final_path = cert_dir / self.default_pem_filename
        else:
            final_path = Path(path).expanduser()
            _ensure_private_dir(final_path.parent, enforce_mode=False)

        if final_path.exists() and not overwrite:
            exc_msg = const._EXCEPTION_CLASSES._PRIVATE_KEY_ALREADY_EXISTS.format(final_path=final_path)
            logger.error(exc_msg)
            raise FileExistsError(exc_msg)

        temp_fd, temp_name = tempfile.mkstemp(
            prefix=f'.{final_path.stem}-',
            suffix=const.FILE_EXTENSIONS.DOT_TMP,
            dir=str(final_path.parent),
        )
        temp_path = Path(temp_name)

        try:
            os.chmod(temp_path, const.CREDENTIAL_VALUES.PRIVATE_FILE_MODE)
            with os.fdopen(temp_fd, 'wb') as temp_file:
                temp_file.write(self.private_key_bytes())
                temp_file.flush()
                os.fsync(temp_file.fileno())

            if final_path.exists() and not overwrite:
                exc_msg = const._EXCEPTION_CLASSES._PRIVATE_KEY_ALREADY_EXISTS.format(final_path=final_path)
                logger.error(exc_msg)
                raise FileExistsError(exc_msg)

            os.replace(temp_path, final_path)
            os.chmod(final_path, const.CREDENTIAL_VALUES.PRIVATE_FILE_MODE)
            return final_path

        except FileExistsError:
            try:
                os.close(temp_fd)
            except OSError:
                pass
            if temp_path.exists():
                temp_path.unlink()
            raise
        except OSError as exc:
            try:
                os.close(temp_fd)
            except OSError:
                pass
            if temp_path.exists():
                temp_path.unlink()
            exc_msg = f"Failed to securely persist the private key to '{final_path}'"
            logger.error(exc_msg)
            raise IDPlusCredentialError(exc_msg) from exc


IDPlusKeyMaterial = IDPlusLegacyKeyMaterial


def from_json_text(text: str) -> IDPlusLegacyKeyMaterial:
    """Parse and validate RSA ID Plus key material from JSON text.

    :param text: JSON content for a `.key` credential file
    :type text: str
    :returns: Parsed and validated key material
    """
    return IDPlusLegacyKeyMaterial.from_json_text(text)


def from_file(path: Union[str, Path]) -> IDPlusLegacyKeyMaterial:
    """Parse and validate RSA ID Plus key material from file.

    :param path: Path to a `.key` credential file
    :returns: Parsed and validated key material
    """
    return IDPlusLegacyKeyMaterial.from_file(path)


def _slugify(value: str) -> str:
    """Return a lowercase, filename-safe slug.

    .. note::
       Invalid characters are replaced with ``-`` and repeated separators are collapsed.

    :param value: The raw value to transform
    :type value: str
    :returns: The sanitized slug value
    :raises: :py:exc:`TypeError`
    """
    if not isinstance(value, str):
        exc_msg = f"The 'value' parameter must be a string (Provided: {type(value)})."
        logger.error(exc_msg)
        raise TypeError(exc_msg)

    slug = value.strip().lower()
    slug = re.sub(r'[^a-zA-Z0-9._-]+', '-', slug)
    slug = re.sub(r'-{2,}', '-', slug)
    return slug.strip('-.')


def _extract_required_string(payload: Mapping[str, Any], field_name: str) -> str:
    """Return a required non-empty string field from parsed key material JSON."""
    if field_name not in payload:
        exc_msg = f"Missing required credential field '{field_name}'."
        logger.error(exc_msg)
        raise IDPlusCredentialError(exc_msg)

    value = payload[field_name]
    if not isinstance(value, str) or not value.strip():
        exc_msg = f"The '{field_name}' credential field must be a non-empty string."
        logger.error(exc_msg)
        raise IDPlusCredentialError(exc_msg)

    return value.strip()


def _extract_optional_string(payload: Mapping[str, Any], field_name: str) -> Optional[str]:
    """Return an optional string field from parsed key material JSON."""
    if field_name not in payload or payload[field_name] is None:
        return None

    value = payload[field_name]
    if not isinstance(value, str):
        exc_msg = f"The optional '{field_name}' credential field must be a string."
        logger.error(exc_msg)
        raise IDPlusCredentialError(exc_msg)

    normalized = value.strip()
    return normalized or None


def _ensure_private_dir(path: Path, enforce_mode: bool) -> None:
    """Ensure a writable directory exists for private key material storage."""
    try:
        path.mkdir(parents=True, exist_ok=True, mode=const.CREDENTIAL_VALUES.PRIVATE_DIR_MODE)
        if enforce_mode:
            os.chmod(path, const.CREDENTIAL_VALUES.PRIVATE_DIR_MODE)
    except OSError as exc:
        exc_msg = f"Failed to prepare the private key directory '{path}'."
        logger.error(exc_msg)
        raise IDPlusCredentialError(exc_msg) from exc


__all__ = [
    'IDPlusLegacyKeyMaterial',
    'IDPlusKeyMaterial',
    'from_json_text',
    'from_file',
]
