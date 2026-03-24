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
- `issuer_url` in `connection_info["oauth"]` or inferable tenant/admin base URL

Token endpoint defaults to: `{issuer_url}/token`

### Argument-Based Example

```python
from pydplus import PyDPlus

pydp = PyDPlus(
    connection_type="oauth",
    base_admin_url="https://example-company.access.securid.com",
    oauth_client_id="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
    oauth_private_key="/path/to/oauth-private-key.jwk",
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
      "issuer_url": "https://example-company.access.securid.com/oauth",
      "client_id": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
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
PYDPLUS_OAUTH_ISSUER_URL=https://example-company.access.securid.com/oauth
PYDPLUS_OAUTH_CLIENT_ID=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
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
