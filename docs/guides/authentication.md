# Authentication

PyDPlus supports two connection types:

- `legacy`
- `oauth`

This guide focuses on practical setup patterns for both, with OAuth using the
Private Key JWT flow for Administration API calls.

## Connection Type Resolution

When `connection_type` is not explicitly set, `PyDPlus` resolves it in this order:

1. Complete OAuth credentials -> `oauth`
2. Complete legacy credentials -> `legacy`
3. Fallback default -> `oauth`

You can always override by passing `connection_type="legacy"` or
`connection_type="oauth"`.

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
- `oauth_scope` (required; plus-delimited, space-delimited, or iterable scope values)
- Optional: `oauth_api_type` (`auth` by default, `admin` supported)

Token endpoint defaults to: `{issuer_url}/token`

When requesting tokens, PyDPlus sends scopes to `/oauth/token` as a space-delimited list and sets
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
  "oauth_scope_preset": "user_read_only",
  "base_urls": {
    "admin": "https://example-company.access.securid.com"
  },
  "connection": {
    "oauth": {
      "issuer_url": "https://example-company.auth.securid.com/oauth",
      "client_id": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
      "scope": "rsa.user.read+rsa.user.manage",
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

## Token Refresh Behavior

For OAuth Admin API requests:

- PyDPlus caches access-token metadata in memory.
- It refreshes the token when expired/near-expiry.
- If an Admin API call returns `401`, PyDPlus forces one token refresh and retries once.

## Notes

- Current OAuth support in PyDPlus is scoped to **Administration API** usage.
- `Client Credentials` and `client_credentials` are both accepted.
- `Private Key JWT` and `private_key_jwt` are both accepted.
- OAuth scope values are required and can be supplied as `+`-delimited, space-delimited, or iterable values.
- OAuth scope presets can be supplied through `oauth_scope_preset` (argument), helper setting, or
  `PYDPLUS_OAUTH_SCOPE_PRESET` (environment variable).
- Scope presets are additive and are merged with explicit `oauth_scope` values; explicit scopes are preserved.
- Scope values are normalized internally and sent to `/oauth/token` as a space-delimited list.
- OAuth issuer inference defaults to the Authentication base URL (`auth` mode).
- When only `base_admin_url` is provided and it matches `*.access.*`, PyDPlus attempts to infer `base_auth_url`.
- Use `oauth_api_type="admin"` to force issuer inference from `base_admin_url`.

## OAuth 403 Troubleshooting

If token requests fail with `403 Forbidden` at `/oauth/token`:

- Verify the configured token issuer host for your tenant.
- Verify `oauth_scope` contains one or more valid, enabled permissions for that OAuth client.
- Set `oauth_issuer_url` directly from the tenant UI issuer value when available.
- If you rely on inferred URLs, provide both `base_admin_url` and `base_auth_url` explicitly.
