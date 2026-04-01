# Quickstart

This quickstart shows the fastest path to:

1. Import `pydplus`
2. Instantiate a `PyDPlus` client
3. Retrieve a User ID using an email address
4. Disable the user within the RSA ID Plus tenant

For setup and environment requirements, see [Overview](overview.md) and
[Installation](installation.md).

## 1. Import The Package

```python
import pydplus
from pydplus import PyDPlus

print(pydplus.__version__)
```

## 2. Instantiate A Client

OAuth is recommended for new integrations. You can keep credentials in a helper file so secrets stay out
of your source code.

```python
from pydplus import PyDPlus, constants as const

pydp = PyDPlus(
    connection_type="oauth",
    base_admin_url="https://example-company.access.securid.com",
    oauth_client_id="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
    oauth_private_key="/path/to/oauth-private-key.jwk",
    oauth_scope=[
        const.OAUTH_SCOPES.USER_READ,
        const.OAUTH_SCOPES.USER_MANAGE,
    ],
)
```

You can also use a helper file:

```python
from pydplus import PyDPlus

pydp = PyDPlus(
    helper="/path/to/helper.json",
)
```

:::{tip}
Need help choosing the authentication pattern? See
[Authentication Guide](../guides/authentication.md), including OAuth scope presets and
scope-strategy options.
:::

## 3. Retrieve a User ID from an email address

Use {py:meth}`~pydplus.PyDPlus.User.get_user_id` to retrieve the User ID for a given user:

```python
user_id = pydp.users.get_user_id(email='john.doe@example.com')

print(f"User ID: {user_id}")
```

## 4. Disable a user

Create a record with {py:meth}`~pydplus.PyDPlus.User.disable_user()`:

```python
response = pydp.users.disable_user(user_id=user_id)
```

## Where To Go Next

- Authentication details and helper-file formats:
  [Authentication Guide](../guides/authentication.md)
- API errors, exceptions, and diagnostics:
  [Error Handling Guide](../guides/error-handling.md)
- Client and method reference:
  [Client API Reference](../reference/client.rst)
