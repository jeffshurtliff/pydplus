---
name: Test Request
about: Request new or improved test coverage for PyDPlus
title: "[TEST] <brief description>"
labels: testing
assignees: ''

---

## Test Request Summary

Describe the test coverage gap or test-suite improvement you are requesting.

What behavior, edge case, or scenario should be tested?

---

## Why This Test Work Is Needed

Explain **why** this testing request matters.

Examples:
- Prevent regression for a known issue
- Increase confidence in a critical code path
- Cover edge cases not currently tested
- Reduce flaky behavior in CI

---

## Target Behavior / Scenario

Describe the behavior or conditions that should be validated.

If applicable, include:
- Inputs
- Expected outputs
- Error conditions
- Boundary/edge cases

---

## Suggested Test Scope (if known)

Check all that apply:

- [ ] Unit tests
- [ ] Regression tests
- [ ] Integration-style tests (isolated/mocked)
- [ ] Fixture improvements
- [ ] Parameterized cases
- [ ] CI reliability/flakiness checks
- [ ] I am not sure

---

## Reproduction / Example Data (Optional)

Provide a minimal example, failing scenario, or pseudocode that shows what should be tested.

```python
# Optional example scenario or expected test shape
```

⚠️ Do not include credentials, tokens, or sensitive org-specific details.

---

## Acceptance Criteria (Optional)

How should maintainers know this request is complete?

Examples:
- Specific edge case is covered
- Regression test added for issue #...
- Flaky path becomes stable across repeated CI runs

---

## Additional Context

Add any other context that may help:
- Related issues or PRs
- Affected RSA APIs or objects
- Prior failures or flaky runs

---

## Willingness to Contribute

- [ ] I am willing to help write tests
- [ ] I can help reproduce or validate scenarios
- [ ] I am only reporting the coverage gap

---

## Final Notes

Thank you for helping improve test coverage and reliability in PyDPlus.  
Focused test requests help prevent regressions and strengthen releases.
