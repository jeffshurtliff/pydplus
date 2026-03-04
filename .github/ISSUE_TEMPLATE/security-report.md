---
name: Security Report
about: Report a potential security concern in PyDPlus (public fallback; sanitize details)
title: "[SECURITY] <brief sanitized summary>"
labels: security
assignees: ''

---

## Important: Public Issue Warning

This issue template creates a **public GitHub Issue**.

If you are reporting a real or suspected vulnerability, the preferred path is **GitHub Private Vulnerability Reporting** (Security tab -> **Report a vulnerability**) so details can be handled privately.

Use this public template only if:
- Private reporting is unavailable, or
- You are sharing a **sanitized, non-sensitive** security concern / hardening suggestion

⚠️ Do **not** include secrets, proof-of-concept exploit payloads, private endpoints, customer/environment details, or step-by-step exploit instructions.

---

## Reporter Checklist

- [ ] I understand this issue will be public
- [ ] I have not included secrets or sensitive data
- [ ] I have sanitized logs, examples, and environment details
- [ ] This report is safe to discuss publicly at a high level

If any box cannot be checked, please use private vulnerability reporting instead.

---

## Security Concern Summary (Sanitized)

Provide a short, high-level description of the concern.

Examples:
- Potential input validation weakness
- Sensitive data may be logged under certain conditions
- Insecure default configuration or behavior

---

## Potential Impact (High Level)

Describe the possible impact without including exploit details.

Examples:
- Credential/token exposure risk
- Injection risk
- Privilege or access control weakness
- Data leakage in logs/errors

---

## Affected Versions / Components (if known)

- PyDPlus version(s):
- Python version(s):
- Affected module(s) / functionality:
- Environment constraints:

---

## Reproduction Context (High Level Only)

Describe the general conditions under which the issue may occur.

Do **not** include:
- Secrets or tokens
- Full exploit payloads
- Detailed attack instructions
- Private org URLs or customer data

```text
High-level reproduction context (sanitized)
```

---

## Evidence / Logs (Redacted, Optional)

If helpful, include **sanitized** log excerpts or error messages.

```text
Paste redacted logs or messages here
```

---

## Suggested Mitigation / Hardening (Optional)

If you have ideas for a fix or mitigation, describe them at a high level.

Examples:
- Input sanitization/validation
- Redaction of sensitive fields in logs
- Safer defaults
- Additional permission checks

---

## Coordination Preference (Optional)

- [ ] I can provide additional details privately if a maintainer requests them
- [ ] I am willing to help validate a fix
- [ ] I prefer not to be contacted beyond issue updates

---

## Additional Context

Add any other context that may help triage this report safely.

---

## Acknowledgements

Thank you for taking the time to report security concerns responsibly.  
Sanitized reports and private disclosures both help improve PyDPlus safely.
