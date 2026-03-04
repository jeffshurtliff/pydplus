---
name: Maintainer Test
about: Internal test coverage or test-suite improvements for PyDPlus
title: "[TEST] <brief description>"
labels: maintainer, testing
assignees: []
---

## Test Summary

Brief description of the test work to be completed.

Examples:
- Add regression coverage for a prior bug
- Improve edge-case coverage
- Refactor fixtures for reliability
- Add tests for existing undocumented behavior

---

## Motivation

Why is this test work needed?

Examples:
- Prevent regressions
- Increase confidence in critical flows
- Cover untested branches
- Improve determinism or reduce flakiness

---

## Scope of Test Changes

Check all that apply:

- [ ] Unit tests
- [ ] Integration tests (mocked / isolated)
- [ ] Regression tests
- [ ] Fixture setup/teardown changes
- [ ] Parameterized scenario expansion
- [ ] Coverage-only initiative
- [ ] Test refactor (no production code changes)

Add notes if needed.

---

## Target Scenarios / Risks

List the primary scenarios, edge cases, or risk areas this work should cover.

Examples:
- Authentication token refresh failures
- Pagination boundaries
- Salesforce API error handling
- Timeout and retry behavior

---

## Checklist

- [ ] Test scope confirmed
- [ ] Tests added or updated
- [ ] Tests are deterministic and isolated
- [ ] Flakiness risk reviewed
- [ ] CI passes
- [ ] Ready to close

---

## Done When

What conditions must be met for this test work to be considered complete?

Examples:
- Target scenarios are covered
- Regression reproduces and is protected by tests
- Test suite remains stable in CI
