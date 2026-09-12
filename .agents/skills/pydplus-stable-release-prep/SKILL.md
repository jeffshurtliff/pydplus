---
name: pydplus-stable-release-prep
description: Prepare and validate PyDPlus stable release candidates by promoting the static Poetry version, finalizing the changelog, running repository checks, and inspecting distributions. Use when promoting a PyDPlus development or prerelease version to stable, not for routine dependency updates or development bumps; stop before commits, pushes, tags, uploads, or GitHub changes unless each action is explicitly authorized.
---

# PyDPlus Stable Release Prep

Prepare a locally validated PyDPlus release candidate that follows the repository's maintainer runbook.
The normal endpoint is a release-readiness report and verified local artifacts, not a commit or publication.

## Read repository authority first

Before changing state, read these files completely from the repository root:

1. `AGENTS.md`
2. `CONTRIBUTING.md`
3. `docs/maintainers/releasing.md`

The runbook is the canonical procedure. This skill supplies PyDPlus-specific
routing and a deterministic artifact check; it does not replace stricter repository instructions.

Inspect `git status --short --branch` before switching branches or editing. Preserve unrelated
work and stop if it cannot be isolated safely.

## Use PyDPlus conventions

- Distribution and import package: `pydplus`
- Version source: static `[project].version` in `pyproject.toml`
- Primary branch: `main`
- Release branch: `chore/<issue>-prepare-<version>-release`
- Stable tag: bare version such as `2.0.1`, created as an annotated tag
- Changelog: `docs/CHANGELOG.md`, including unique MyST targets and comparison links
- Build frontend: Poetry, producing one source distribution and one pure-Python wheel
- Documentation: Sphinx with MyST; treat warnings as failures
- Supported Python versions and dependency floors: always derive from current `pyproject.toml` and CI rather than copying old values

Use the public repository metadata already tracked in the project. Never copy personal filesystem
paths, private instance details, credentials, tokens, helper-file contents, or environment-specific
identifiers into source, documentation, artifacts, commits, or release notes.

## Preserve authorization boundaries

A request to prepare the release authorizes reversible local work: read-only remote checks, creation
or use of the policy-compliant local branch, version and changelog edits, documentation updates,
validation, local builds, archive inspection, and temporary-environment smoke tests.

Require explicit authorization for each applicable external or history-changing action:

- creating or changing a GitHub issue, pull request, or release;
- staging, committing, merging, or pushing release changes;
- creating or pushing a release tag;
- uploading to TestPyPI or PyPI; or
- publishing, editing, or deleting externally visible release state.

Authorization for one action does not authorize later actions. By default, stop before staging or committing.

## Resolve the release facts

Confirm the exact stable version, current prerelease version, release date, issue number, previous
reachable stable tag, target tag, release branch, repository remote, and required checks. Removing
a prerelease suffix is acceptable only when the intended target is unambiguous, such
as `2.0.1.dev0` to `2.0.1`. Never invent an issue number, reuse an existing tag or PyPI version,
or guess the next development version.

The issue number refers to the release's dedicated tracking issue, opened from the **Maintainer
Release** template (`.github/ISSUE_TEMPLATE/maintainer-release.md`) with the `chore/` branch prefix.
If no such issue exists, continue read-only preflight and ask for the issue number before creating the release branch. Do not create an issue without authorization.

Treat an unavailable remote or PyPI check as unresolved rather than proof that the version is unused.
Do not open `local/`, `.env`, home-directory secret stores, decrypted helpers, or encrypted credential
material merely to check release readiness.

## Perform local preparation

Follow runbook sections 1 through 5 and complete all local preparation checks before handing off:

1. Review the full change set since the prior stable tag and confirm release scope.
2. Establish the clean release branch from current `main` according to the issue policy.
3. Promote the exact stable version with `poetry version`; never edit `poetry.lock` manually or refresh dependencies incidentally.
4. Move `Unreleased` entries into the dated release section, reset the existing category skeleton with placeholders, rename MyST targets, and update comparison links.
5. Search maintained source, docs, workflows, tests, examples, and metadata for stale prerelease wording. Preserve historical references.
6. Run every repository release check, including Poetry lock validation, Ruff lint and format checks, pytest, Bandit, the clean warning-as-error Sphinx build, and `git diff --check`.
7. Recommend integration validation when an authorized ID Plus test environment is available; appropriately mocked checks may also be run. If environment access is not feasible, report validation as skipped with the reason. This skip does not block release readiness. Distinguish real and mocked results, and investigate failures from checks that are run before declaring readiness. Never inspect or expose credential-bearing configuration to determine environment availability.
8. Build clean candidate archives and require strict Twine validation.

Build into the new temporary `RELEASE_DIST_DIR` specified by the runbook; preserve existing `dist/` artifacts.
After the build, run the repository-owned inspector from the repository root:

```bash
poetry run python .agents/skills/pydplus-stable-release-prep/scripts/inspect_release_artifacts.py \
  --dist-dir "$RELEASE_DIST_DIR" \
  --expected-version "$RELEASE_VERSION" \
  --strict
```

First install the wheel with `--no-deps` in a new temporary virtual environment and assert `importlib.metadata.version('pydplus')`. Then use a second clean virtual environment to install the wheel normally with its runtime dependencies and confirm `from pydplus import PyDPlus` succeeds. Do not require the public import in the dependency-free environment. These smoke tests supplement, but never replace, CI across all supported Python versions.

Review `git status`, the complete diff, generated-file ignore behavior, and candidate checksums. Fix in-scope failures and rerun affected and dependent checks. Do not weaken tests, dependency floors, lint rules, archive checks, or documentation warnings to obtain a passing result.

## Stop and report

Unless the user has explicitly authorized a later action, stop before runbook section 6. Report:

- resolved release facts and assumptions;
- each changed file and why it changed;
- every check with pass, fail, or intentionally skipped status;
- artifact filenames and SHA-256 checksums;
- blockers and manual reviews still required; and
- the exact next action requiring authorization.

If the user later authorizes publication work, reread the corresponding runbook section, revalidate
its prerequisites, and perform only the specifically authorized action. Never reuse pre-merge candidate
archives for publication.
