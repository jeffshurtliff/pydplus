---
name: Maintainer Security
about: Internal security tracking and hardening work for PyDPlus maintainers
title: "[SECURITY] <brief description>"
labels: maintainer, security
assignees: []
---

## Security Summary

Brief description of the security issue, mitigation, or hardening work.

⚠️ If sensitive vulnerability details are involved, coordinate in a private security advisory first and use this issue only for non-sensitive tracking notes.

---

## Risk / Impact Assessment

Describe the security risk at a high level.

Consider including:
- Affected trust boundary
- Potential impact (credential exposure, injection, privilege misuse, etc.)
- Likelihood or exploitability (if known)
- Severity estimate (informal or formal)

---

## Affected Components / Versions

List the impacted areas, if known.

- Module(s) / code path(s):
- Version(s) affected:
- Environment constraints (if any):

---

## Root Cause / Threat Model (if known)

Describe the root cause or security weakness.

Examples:
- Missing input validation
- Unsafe defaults
- Sensitive data logged
- Insufficient permission checks
- Insecure dependency usage

If not yet confirmed, capture hypotheses and investigation notes.

---

## Remediation Plan

Outline the planned mitigation or fix.

Optional notes:
- Code changes
- Dependency updates
- CI/security scanning updates
- Documentation or guidance updates
- Backport considerations

---

## Validation / Verification

How will the mitigation be validated?

Examples:
- Regression/security tests added
- Manual verification of exploit path blocked
- Static analysis or CI scan confirmation
- Review of logging/redaction behavior

---

## Disclosure / Coordination

Check all that apply:

- [ ] Private disclosure path used (advisory/private report)
- [ ] Public issue is sanitized (no sensitive exploit details)
- [ ] Coordinated release timing needed
- [ ] Backport(s) required
- [ ] Changelog / security note required
- [ ] CVE/CWE tracking needed

Add notes if relevant.

---

## Checklist

- [ ] Risk assessed
- [ ] Fix or mitigation implemented
- [ ] Verification complete
- [ ] Documentation updated (if applicable)
- [ ] Release coordination reviewed (if applicable)
- [ ] Ready to close

---

## Done When

What conditions must be met for this security work to be considered complete?

Examples:
- Vulnerability is mitigated or risk reduced as intended
- Sensitive data is no longer exposed
- Verification confirms expected protections
