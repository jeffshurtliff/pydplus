# Contributing to PyDPlus

Thank you for your interest in contributing to **PyDPlus**.

This project is maintained with strict standards for structure, naming, documentation, security, and semantic 
versioning. While the repository is currently maintained by a single maintainer, external contributions are 
welcome — provided they adhere closely to the conventions defined below.

Please read this document in full before opening an issue or submitting a pull request.

---

## Guiding Principles

PyDPlus is built around the following principles:

- Clean, intuitive, and scalable architecture
- Strict adherence to PEP 8
- Clear public API boundaries
- Security-first design
- Strong test coverage
- Comprehensive documentation
- Predictable semantic versioning
- Explicit and consistent Git workflow

All contributions must align with these principles.

---

## Development Workflow Overview

1. Open or reference a GitHub Issue before beginning work.
2. Use the correct Issue template.
3. Create a properly-prefixed branch from `main`.
4. Include the Issue number in the branch name.
5. Write or update tests as appropriate.
6. Update documentation when necessary.
7. Ensure CI passes before requesting review.

---

## Branch Naming Convention

All branches **must** follow the structured prefix system below.

Branch names must include:

```
<prefix>/<issue-number>-short-description
```

### Example

If addressing GitHub Issue **#13** for a bug:

```
fix/13-increase-timeout-length
```

The Issue number must appear immediately after the prefix.

---

## Issue and Prefix Types

The sections below explain the different types/categories and when they should be used.

Valid prefixes:

- Feature (`feature/`)
- Bug (`fix/`)
- Refactor (`refactor/`)
- Chore (`chore/`)
- Documentation (`docs/`)
- Test (`test/`)
- CI (`ci/`)
- Security (`security/`)

---

> **Important**
>
> The branch name examples below are generic.
> 
> In actual usage, include the Issue number immediately after the prefix.
> 
> Example:
> ```
> feature/42-async-client
> ```

---

### Feature - User-Visible Capability

| Aspect                     | Value                                                               |
|----------------------------|---------------------------------------------------------------------|
| Issue Template: Maintainer | Maintainer Feature                                                  |
| Issue Template: Requester  | Feature Request                                                     |
| Issue Subject Prefix       | `[FEATURE]`                                                         |
| Label(s)                   | Maintainer: `enhancement`, `maintainer`<br>Requester: `enhancement` |
| Branch Prefix              | `feature/`                                                          |

#### Criteria

A change is considered a **feature** when it:

- Adds new public API surface (new classes, methods, decorators, CLI commands, etc.)
- Enables new functionality for consumers of the library
- Changes behavior in a way users can observe
- Requires documentation updates explaining new capability
- May justify a **minor version bump** under semantic versioning

#### Examples

- `feature/bulk-enable-support`
- `feature/typed-response-models`
- `feature/async-client`
- `feature/retry-strategy-configuration`

#### Litmus Test

Would a user upgrading the package say:

> “Oh cool, this does something new now.”

If yes → `feature/`.

---

### Fix - Defect / Bug Fix

| Aspect                     | Value                                               |
|----------------------------|-----------------------------------------------------|
| Issue Template: Maintainer | Maintainer Bug                                      |
| Issue Template: Requester  | Bug Report                                          |
| Issue Subject Prefix       | `[BUG]`                                             |
| Label(s)                   | Maintainer: `bug`, `maintainer`<br>Requester: `bug` |
| Branch Prefix              | `fix/`                                              |

#### Criteria

A change is considered a **bug** when it:

- Corrects incorrect behavior
- Resolves a regression
- Fixes security flaws
- Addresses incorrect documentation tied to behavior

#### Examples

- `fix/query-pagination-loop`
- `fix/oauth-token-refresh`
- `fix/incorrect-error-raising`

#### Litmus Test

Is this correcting something that already *should have worked*?

If yes → `fix/`.

---

### Refactor - Internal Structural Change (No Behavior Change)

| Aspect                     | Value                                                         |
|----------------------------|---------------------------------------------------------------|
| Issue Template: Maintainer | Maintainer Refactor                                           |
| Issue Template: Requester  | Refactor Request                                              |
| Issue Subject Prefix       | `[REFACTOR]`                                                  |
| Label(s)                   | Maintainer: `refactor`, `maintainer`<br>Requester: `refactor` |
| Branch Prefix              | `refactor/`                                                   |

#### Criteria

A change is considered a **refactor** when it:

- Reorganizes modules
- Improves internal design
- Extracts shared logic
- Changes implementation without changing behavior
- Improves testability or maintainability
- Moves logic into utilities, services, etc.

#### Examples

- `refactor/split-client-module`
- `refactor/extract-auth-logic`
- `refactor/standardize-exceptions`
- `refactor/centralize-constants`

#### Litmus Test

If all tests ran before and after, would behavior be identical?

If yes → `refactor/`.

---

### Chore - Maintenance, Tooling, or Non-Functional Work

| Aspect                     | Value                                               |
|----------------------------|-----------------------------------------------------|
| Issue Template: Maintainer | Maintainer Chore                                    |
| Issue Template: Requester  | N/A                                                 |
| Issue Subject Prefix       | `[CHORE]`                                           |
| Label(s)                   | Maintainer: `chore`, `maintainer`<br>Requester: N/A |
| Branch Prefix              | `chore/`                                            |

#### Criteria

A change is considered a **chore** when it:

- Updates dependencies
- Adjusts project metadata
- Improves packaging configuration
- Updates linting or formatting rules
- Performs minor cleanup not tied to design improvement
- Updates documentation that does not affect behavior

#### Examples

- `chore/update-dependencies`
- `chore/poetry-config-cleanup`
- `chore/add-pre-commit-hooks`
- `chore/rename-test-files`

#### Litmus Test

Is this maintenance work that does not improve architecture or add capability?

If yes → `chore/`.

---

### Documentation - Documentation-Only Changes

| Aspect                     | Value                                                                   |
|----------------------------|-------------------------------------------------------------------------|
| Issue Template: Maintainer | Maintainer Docs                                                         |
| Issue Template: Requester  | Docs Request                                                            |
| Issue Subject Prefix       | `[DOCS]`                                                                |
| Label(s)                   | Maintainer: `documentation`, `maintainer`<br>Requester: `documentation` |
| Branch Prefix              | `docs/`                                                                 |

#### Criteria

A change is considered **documentation-only** when it:

- Updates docstrings
- Improves Sphinx or MyST content
- Fixes typos or formatting
- Clarifies usage examples
- Adds documentation for existing features
- Updates README content
- Improves API reference descriptions

#### Examples

- `docs/improve-authentication-guide`
- `docs/add-bulk-query-example`
- `docs/fix-typos-in-readme`
- `docs/update-installation-instructions`
- `docs/add-type-hint-explanations`

#### Litmus Test

Does this change only documentation and not runtime behavior?

If yes → `docs/`.

#### Important Distinction

- Fixing incorrect documentation because behavior was wrong → `fix/`
- Updating docs because you added new functionality → `feature/`
- Adjusting documentation build pipeline → `ci/`

---

### Test - Test-Only Changes

| Aspect                     | Value                                                       |
|----------------------------|-------------------------------------------------------------|
| Issue Template: Maintainer | Maintainer Test                                             |
| Issue Template: Requester  | Test Request                                                |
| Issue Subject Prefix       | `[TEST]`                                                    |
| Label(s)                   | Maintainer: `testing`, `maintainer`<br>Requester: `testing` |
| Branch Prefix              | `test/`                                                     |

#### Criteria

A change is considered **test-only** when it:

- Adds new test coverage
- Improves existing tests
- Refactors test structure
- Improves fixtures
- Adds regression tests
- Strengthens edge case coverage
- Adds security-focused tests
- Increases coverage percentage without modifying production logic

#### Examples

- `test/add-pagination-edge-cases`
- `test/increase-auth-coverage`
- `test/add-regression-for-issue-142`
- `test/refactor-fixture-structure`
- `test/improve-mock-isolation`

#### Litmus Test

Does this modify only the test suite and not production code?

If yes → `test/`.

#### Advanced OSS Discipline

- Adding regression tests after a bug fix → separate `test/` branch
- Fix + test together → typically `fix/`
- Coverage improvement initiative → `test/`

---

### CI - Continuous Integration / Automation

| Aspect                     | Value                                             |
|----------------------------|---------------------------------------------------|
| Issue Template: Maintainer | Maintainer CI                                     |
| Issue Template: Requester  | CI Request                                        |
| Issue Subject Prefix       | `[CI]`                                            |
| Label(s)                   | Maintainer: `ci`, `maintainer`<br>Requester: `ci` |
| Branch Prefix              | `ci/`                                             |

#### Criteria

A change is considered **CI-related** when it:

- Modifies GitHub Actions workflows
- Updates CodeQL or Bandit configuration
- Adjusts test matrix
- Improves release automation
- Updates Dependabot configuration
- Adjusts coverage upload behavior
- Modifies RTD build configuration
- Changes CI-only pre-commit behavior

#### Examples

- `ci/update-python-matrix`
- `ci/add-codeql-analysis`
- `ci/fix-release-workflow`
- `ci/add-bandit-sarif-upload`
- `ci/improve-coverage-reporting`

#### Litmus Test

Does this change affect only automation or pipelines, not the library itself?

If yes → `ci/`.

#### Important Distinction

- Updating dependency versions in `pyproject.toml` → `chore/`
- Updating how CI installs dependencies → `ci/`
- Improving packaging metadata → `chore/`

CI is for pipeline mechanics.  
Chore is for repository maintenance.

---

### Security - Security-Related Improvements

| Aspect                     | Value                                                         |
|----------------------------|---------------------------------------------------------------|
| Issue Template: Maintainer | Maintainer Security                                           |
| Issue Template: Requester  | Security Report                                               |
| Issue Subject Prefix       | `[SECURITY]`                                                  |
| Label(s)                   | Maintainer: `security`, `maintainer`<br>Requester: `security` |
| Branch Prefix              | `security/`                                                   |

> **Responsible Security Reporting**
>
> If you believe you found a real vulnerability, prefer **GitHub Private Vulnerability Reporting**
> (Security tab -> "Report a vulnerability") instead of opening a public issue.
>
> The public **Security Report** issue template is a fallback for sanitized reports only
> (for example: low-risk concerns, hardening suggestions, or when private reporting is unavailable).
>
> Do **not** post exploit details, proof-of-concept payloads, secrets, or sensitive environment data in public Issues.

#### Criteria

A change is considered **security-related** when it:

- Fixes a vulnerability
- Improves input validation
- Hardens authentication logic
- Removes unsafe defaults
- Updates cryptographic usage
- Addresses CVEs
- Improves token handling
- Strengthens request verification
- Tightens permission checks
- Rotates secrets in CI
- Mitigates injection risks
- Prevents sensitive data exposure in logs

#### Examples

- `security/sanitize-query-input`
- `security/harden-token-storage`
- `security/remove-unsafe-defaults`
- `security/fix-cve-urllib3-2026`
- `security/prevent-header-injection`

#### Litmus Test

Is this change primarily focused on reducing security risk?

If yes → `security/`.

#### Versioning Guidance

Security changes typically justify:

- Patch bump (no API change)
- Minor bump (stricter behavior)
- Rarely major (breaking change required for safety)

---

## Code Standards

All contributions must:

- Follow PEP 8
- Use type hints where appropriate that support Python 3.9+
- Maintain or increase test coverage
- Avoid introducing public API instability without justification
- Avoid adding third-party dependencies unless strongly justified
- Preserve backward compatibility unless explicitly approved

### Linting and Formatting

PyDPlus uses [Ruff](https://docs.astral.sh/ruff/) for linting, import sorting, and code formatting.
The repository standard is a maximum line length of `130` characters.

Line-length policy:

- Keep production code, tests, and normal string expressions at or under 130 characters.
- Prefer refactoring/wrapping code over suppressing line-length violations.
- Overriding line length is permitted only for comments and special situations where readability would be reduced by wrapping
  (for example: unavoidable literal examples, externally-defined tokens, or similarly constrained values).
- Use per-line `# noqa: E501` for approved exceptions instead of broad file-level or global ignores.

Before opening a PR, run:

```bash
poetry run ruff check .
poetry run ruff check . --fix
poetry run ruff format .
poetry run ruff format . --check
```

CI enforces these Ruff checks.

---

## Testing Requirements

- All new behavior must include tests.
- All bug fixes must include regression tests.
- CI must pass before PR approval.
- CI enforces a minimum total test coverage threshold of 50%.
- Tests must be deterministic and isolated.
- Keep test modules under `tests/`.
- Avoid unnecessary mocking when integration tests are more appropriate.

---

## Documentation Requirements

If you:

- Add a feature → update documentation.
- Change behavior → update documentation.
- Modify public API → update docstrings and usage examples.

Documentation must remain consistent with the published version.

---

## Documentation Policy and Standards

PyDPlus documentation must remain clear, user-focused, and free of implementation noise.

The purpose of documentation is to describe the public contract of the library — not its internal structure.

---

### Documentation Philosophy

Documentation should:

- Describe what the library does
- Explain how to use the public API
- Clarify behavior and edge cases
- Document error conditions
- Provide examples where helpful
- Reflect observable behavior

Documentation should **not**:

- Describe internal refactors
- Explain implementation restructuring
- Document private helper functions
- Record maintenance history
- Duplicate CHANGELOG entries
- Expose internal architectural details unless intentionally public

If a change does not affect users, it should not appear in user-facing documentation.

---

### Public vs Internal API Documentation

Only public interfaces must be documented.

Public API includes:

- Public classes
- Public methods
- Public functions
- Public exceptions
- Public decorators
- Documented constants intended for consumer usage

Private or internal items (prefixed with `_`) should not be included in narrative documentation and should not receive version directives.

If a module or constant is internal-only, do not surface it in the docs.

---

### Version Directives Policy

Sphinx directives such as:

- `.. versionadded::`
- `.. versionchanged::`
- `.. deprecated::`

Must only be used when:

- Public behavior changes
- Public signatures change
- Return values change
- Exceptions change
- Default behavior changes
- Deprecations are introduced
- Security changes affect behavior
- Performance characteristics meaningfully change

Do not use version directives for:

- Internal refactors
- Code reorganization
- Moving constants
- Renaming private helpers
- Documentation wording improvements
- Test restructuring

Implementation changes belong in the CHANGELOG, not in docstrings.

---

### CHANGELOG vs Documentation

The CHANGELOG records:

- Refactors
- Dependency updates
- Maintenance work
- CI improvements
- Tooling updates
- Internal restructuring

The documentation describes:

- Current behavior
- Current usage
- Current API contract

Documentation should always describe the present state of the library — not its historical evolution.

---

### Docstring Standards

Docstrings must:

- Follow consistent reStructuredText format
- Include type hints in signatures (not repeated redundantly)
- Document parameters and return values clearly
- Document raised exceptions when applicable
- Avoid excessive verbosity
- Avoid implementation detail leakage

Docstrings should explain:

- What the function does
- What it expects
- What it returns
- When it raises exceptions
- Any important usage caveats

Docstrings should not explain:

- Internal helper calls
- Refactoring rationale
- Internal constant usage
- Code structure

---

### Deprecation Policy

When deprecating a public API:

1. Add a `.. deprecated::` directive.
2. Add the `@deprecated` decorator (with `since`, `replacement`, and `removal` parameters as applicable).
3. Document the recommended alternative.
4. Maintain backward compatibility during the deprecation window.
5. Update narrative documentation accordingly.
6. Add CHANGELOG entry under "Deprecated".

Removal of deprecated functionality must align with semantic versioning rules.

---

### Documentation Cleanliness Requirements

Contributors must ensure:

- No dead references
- No broken cross-references
- No outdated examples
- No references to removed APIs
- No copy/paste errors from prior versions

CI failures due to documentation warnings must be resolved before merging.

---

### Examples and Usage Clarity

Code examples must:

- Be minimal and realistic
- Use public API only
- Avoid private attributes
- Avoid exposing internals
- Be syntactically correct
- Prefer clarity over cleverness

Examples should reflect recommended usage patterns.

---

### Security Documentation Guidelines

Documentation must never:

- Include real tokens
- Include sensitive headers
- Include private endpoints
- Show insecure defaults

Security-sensitive examples should use placeholder values.

---

### Stable vs Latest Documentation

The `stable` documentation must reflect the latest release.

The `latest` documentation may reflect unreleased changes, but:

- Must not contradict documented behavior
- Must remain coherent
- Must not expose incomplete APIs without clear intent

---

### Documentation Review Standard

Before merging a PR:

- Confirm public API documentation matches code.
- Confirm new features are documented.
- Confirm removed behavior is no longer documented.
- Confirm version directives (if any) are appropriate and necessary.
- Confirm no internal-only refactors appear in user-facing docs.

Clean documentation is considered part of the public contract of PyDPlus.

---

## Security Expectations

PyDPlus interacts with authentication flows and API tokens. Contributions must:

- Avoid logging secrets.
- Avoid insecure defaults.
- Validate user input where applicable.
- Use secure standard libraries whenever possible.
- Justify any cryptographic or authentication changes.
- Use private vulnerability reporting for sensitive disclosures whenever possible.

Security-related contributions may receive heightened review scrutiny.

---

## Pull Request Requirements

Every PR must:

- Reference a GitHub Issue.
- Use the correct branch prefix.
- Pass CI.
- Include tests when applicable.
- Include documentation updates when applicable.
- Maintain semantic versioning integrity.

PRs that do not follow naming or structural rules may be closed without review.

---

## Manual Release Preflight Checklist

Before cutting a release, run the following checks from the repository root:

```bash
poetry check
poetry run ruff check .
poetry run ruff format --check .
poetry run pytest --run-integration -q
poetry run bandit -r src
poetry run sphinx-build -b html docs docs/_build/html
poetry build
poetry run python -m twine check dist/*
```

For manual releases, the maintainer is responsible for final release actions:

- Push/merge release-ready changes to `origin/main`
- Create the release tag (for example `1.0.0`)
- Publish artifacts to PyPI
- Create the GitHub release notes entry

---

## Final Notes

Consistency is more important than speed.

Clear intent in branch names and Issues improves long-term maintainability, release hygiene, and contributor clarity.

Thank you for helping maintain a clean, professional, and secure codebase.
