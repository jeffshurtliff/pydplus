# Authentication

PyDPlus supports two connection types:

- `legacy`
- `oauth`

For new integrations, OAuth (Private Key JWT) is recommended.

## Connection Type Resolution

When `connection_type` is not explicitly set, `PyDPlus` resolves it in this order:

1. Complete OAuth credentials -> `oauth`
2. Complete legacy credentials -> `legacy`
3. Fallback default -> `oauth`

You can always override with `connection_type="legacy"` or `connection_type="oauth"`.

## Legacy Authentication

Legacy auth requires:

- `legacy_access_id`
- private key material (`private_key` path or key material from helper/env)

Example:

```python
from pydplus import PyDPlus

pydp = PyDPlus(
    connection_type="legacy",
    base_admin_url="https://example-company.access.securid.com",
    legacy_access_id="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
    private_key="/path/to/legacy-private-key.pem",
)
```

## OAuth Authentication (Admin API)

OAuth (Private Key JWT) requires:

- `oauth_client_id`
- `oauth_private_key` (path to `.jwk`) or `oauth_private_key_jwk` (inline JWK)
- `issuer_url` (`oauth_issuer_url` argument, `connection_info["oauth"]["issuer_url"]`, or inferred from base URLs)
- `oauth_scope` (required; `+`-delimited, space-delimited, comma-delimited, or iterable values)
- Optional: `oauth_api_type` (`auth` by default, `admin` supported)

Token endpoint defaults to: `{issuer_url}/token`

When requesting tokens, PyDPlus sends scopes to `/oauth/token` as a space-delimited value and sets
`Content-Type: application/x-www-form-urlencoded; charset=UTF-8`.

### Argument-Based Example

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

### Explicit Issuer URL Example

```python
from pydplus import PyDPlus

pydp = PyDPlus(
    connection_type="oauth",
    base_admin_url="https://example-company.access.securid.com",
    oauth_issuer_url="https://example-company.auth.securid.com/oauth",
    oauth_client_id="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
    oauth_private_key="/path/to/oauth-private-key.jwk",
    oauth_scope="rsa.user.read+rsa.user.manage",
)
```

### Helper File Example

```json
{
  "connection_type": "oauth",
  "base_urls": {
    "admin": "https://example-company.access.securid.com"
  },
  "connection": {
    "oauth": {
      "issuer_url": "https://example-company.auth.securid.com/oauth",
      "client_id": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
      "scope": "rsa.user.read+rsa.user.manage",
      "scope_preset": "user_read_only",
      "grant_type": "Client Credentials",
      "client_authentication": "Private Key JWT",
      "private_key_path": "/path/to/keys",
      "private_key_file": "oauth-private-key.jwk"
    }
  }
}
```

### Environment Variable Example

```bash
PYDPLUS_CONNECTION_TYPE=oauth
PYDPLUS_ADMIN_BASE_URL=https://example-company.access.securid.com
PYDPLUS_OAUTH_ISSUER_URL=https://example-company.auth.securid.com/oauth
PYDPLUS_OAUTH_CLIENT_ID=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
PYDPLUS_OAUTH_SCOPE=rsa.user.read+rsa.user.manage
PYDPLUS_OAUTH_SCOPE_PRESET=user_read_only
PYDPLUS_OAUTH_PRIVATE_KEY_FILE=oauth-private-key.jwk
PYDPLUS_OAUTH_PRIVATE_KEY_PATH=/path/to/keys
```

The canonical environment-variable names are available from `const.ENV_VARIABLES`, for example
`const.ENV_VARIABLES.OAUTH_SCOPE` and `const.ENV_VARIABLES.OAUTH_SCOPE_PRESET`.

## OAuth Scope Strategies

Use one of these patterns based on how your team manages permissions.
For official permission descriptions, see RSA's
[OAuth 2.0-based permissions reference](https://community.rsa.com/s/article/OAuth-2-0-Based-Permissions-for-the-Cloud-Administration-APIs-27c2ca90).

### 1) Configure default scopes in RSA Cloud Administration Console

In the OAuth client configuration, set the default permissions your integration should use.
This gives your tenant-side configuration a stable baseline for permissions.

In PyDPlus, still provide `oauth_scope` (directly, helper file, or environment variable) so token requests are explicit,
repeatable, and validated before requests are made.

### 2) Define scopes explicitly (manual or constants)

You can pass raw scope strings:

```python
oauth_scope = "rsa.user.read+rsa.user.manage"
```

Or define a reusable constant-style variable with typed scope values from `const.OAUTH_SCOPES`:

```python
from pydplus import constants as const

OAUTH_SCOPE = [
    const.OAUTH_SCOPES.USER_READ,
    const.OAUTH_SCOPES.USER_MANAGE,
]
```

### 3) Use OAuth scope presets

Presets are named bundles of scopes passed via `oauth_scope_preset` (argument),
`connection.oauth.scope_preset` (helper setting), or `PYDPLUS_OAUTH_SCOPE_PRESET` (environment variable).

Supported preset names:

- `all`, `admin`, `auth`
- `agent`, `audit`, `authenticator`, `fido`, `group`, `report`, `user`
- `all_read_only`, `agent_read_only`, `authenticator_read_only`, `fido_read_only`
- `group_read_only`, `report_read_only`, `user_read_only`

Preset behavior:

- Presets are additive and merge with explicit `oauth_scope` values.
- Duplicate scopes are removed.
- Invalid preset names are ignored (with warning logs).
- Final scope values are normalized internally and submitted to `/oauth/token` as space-delimited values.

Example:

```python
from pydplus import PyDPlus, constants as const

pydp = PyDPlus(
    connection_type="oauth",
    base_admin_url="https://example-company.access.securid.com",
    oauth_client_id="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
    oauth_private_key="/path/to/oauth-private-key.jwk",
    oauth_scope=const.OAUTH_SCOPES.USER_MANAGE,
    oauth_scope_preset=("user_read_only", "group_read_only"),
)
```

## Token Refresh Behavior

For OAuth Admin API requests:

- PyDPlus caches access-token metadata in memory.
- It refreshes the token when expired or near-expiry.
- If an Admin API call returns `401`, PyDPlus forces one token refresh and retries once.

## Additional Notes

- Current OAuth support in PyDPlus is scoped to **Administration API** usage.
- `Client Credentials` and `client_credentials` are both accepted.
- `Private Key JWT` and `private_key_jwt` are both accepted.
- OAuth issuer inference defaults to the Authentication base URL (`auth` mode).
- When only `base_admin_url` is provided and it matches `*.access.*`, PyDPlus attempts to infer `base_auth_url`.
- Use `oauth_api_type="admin"` to force issuer inference from `base_admin_url`.

## OAuth 403 Troubleshooting

If token requests fail with `403 Forbidden` at `/oauth/token`:

- Verify the configured token issuer host for your tenant.
- Verify `oauth_scope` contains one or more valid, enabled permissions for that OAuth client.
- Set `oauth_issuer_url` directly from the tenant UI issuer value when available.
- If you rely on inferred URLs, provide both `base_admin_url` and `base_auth_url` explicitly.
