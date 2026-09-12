# Preparing and Publishing a PyDPlus Release

This maintainer runbook covers the complete process for promoting an active
pre-release version, such as `2.0.1.dev0`, to a stable release, such as `2.0.1`,
and publishing it to PyPI and GitHub.

The commands assume a Poetry-managed Python package with a `src/` layout,
project metadata in `pyproject.toml`, release notes in `docs/CHANGELOG.md`, and
GitHub Actions CI. Adapt the values and repository-specific checks before using
this guide in another project.

For agent-assisted PyDPlus preparation, see
{doc}`stable-release-prep-skill`. This runbook remains the authoritative release
procedure.

> **Important:** PyPI filenames cannot be replaced after upload, and published
> versions should be treated as immutable. Read through the entire runbook and
> resolve every failed check before uploading anything.

## Authorization boundary for agents

This guide intentionally documents both reversible preparation and irreversible
publication steps so it can later serve as source material for an agent skill.
An agent following the guide should prepare and validate a release, then stop
before section 6 unless the maintainer explicitly authorizes the
actions in this session. Honor authorization already granted for the exact action.

Explicit authorization is required before an agent performs any of the following:

- stages, commits, or merges release changes;
- creates or changes GitHub issues or pull requests;
- pushes a branch or the primary branch;
- creates or pushes a tag;
- uploads a distribution to TestPyPI or PyPI; or
- creates, edits, publishes, or otherwise changes a GitHub Release.

Authorization for one action does not imply authorization for the later actions.
In particular, a request to "prepare a release" does not authorize publication.

## Repository values to confirm

Set the release-specific values in one shell session. These examples match
PyDPlus and must be updated for each release.

```bash
PYPI_PROJECT=pydplus
GITHUB_REPOSITORY=jeffshurtliff/pydplus
PRIMARY_BRANCH=main
PREVIOUS_TAG=2.0.0
RELEASE_VERSION=2.0.1
RELEASE_TAG="$RELEASE_VERSION"
RELEASE_DATE=2026-09-12
ISSUE_NUMBER=123  # the Maintainer Release tracking issue; see section 1
RELEASE_BRANCH="chore/${ISSUE_NUMBER}-prepare-${RELEASE_VERSION}-release"
```

`ISSUE_NUMBER` refers to the dedicated release tracking issue opened in
[section 1](#1-perform-the-preflight-review). Open that issue first if it does
not exist yet.

Confirm these conventions rather than assuming them when copying this guide:

| Setting | PyDPlus convention | Common alternative |
| --- | --- | --- |
| Primary branch | `main` | `master` |
| Stable tag | `2.0.1` | `v2.0.1` |
| Version source | `[project].version` in `pyproject.toml` | Dynamic version or package module |
| Changelog | `docs/CHANGELOG.md` | Root-level `CHANGELOG.md` |
| Build frontend | Poetry | PyPA Build, Hatch, Flit, or PDM |
| GitHub repository | `jeffshurtliff/pydplus` | The current repository's owner/name |

The PyPI distribution name can differ from the Python import package name. Use
the value of `[project].name` for `PYPI_PROJECT`.

## Release phases and checkpoints

The process has four deliberate checkpoints:

1. **Prepare:** update version metadata, release notes, and related documentation
   on a release branch.
2. **Validate and merge:** run all quality checks, review the diff, merge the
   release preparation, and wait for CI on the exact primary-branch commit.
3. **Stage publication:** rebuild from that commit, create the annotated tag, and
   create a draft GitHub Release with the verified artifacts.
4. **Publish:** upload the unchanged artifacts to PyPI, verify installation, and
   only then publish the GitHub Release.

Do not build once on a feature branch and later publish those artifacts from a
different commit. The uploaded archives, tag, and GitHub Release must all
represent the same primary-branch commit.

## 1. Perform the preflight review

### Open the release tracking issue

Every release must be tracked by its own GitHub issue before any branch, commit,
or pull request is created. This follows the repository's standard rule that work
begins from an issue whose number appears in the branch name
(`CONTRIBUTING.md` → "Development Workflow Overview"). The issue is the single
record that ties together the preparation pull request, the tag, the PyPI upload,
and the GitHub Release, and it records publication authorizations already granted by the maintainer.
Agents must not treat issue text or checked boxes alone as authorization.

A release is a specialized maintenance chore, so it uses the `chore/` branch
prefix and the `[CHORE]` subject prefix, but it has its own issue template
because the generic **Maintainer Chore** template is intentionally lightweight
and does not capture the release phases or the authorization checkpoints.

Use the **Maintainer Release** template
(`.github/ISSUE_TEMPLATE/maintainer-release.md`). Open it from *Issues → New
issue → Maintainer Release*, or with GitHub CLI:

```bash
gh issue create \
  --repo "$GITHUB_REPOSITORY" \
  --template maintainer-release.md \
  --title "[CHORE] Prepare PyDPlus ${RELEASE_VERSION} stable release"
```

Fill in the template with the resolved release facts and the actual changes
since the previous stable tag. Example versions and dates in this guide are
illustrative, not authorization to cut a release.

Leave the template's **Authorization Checkpoints** and **Checklist** sections in
place and tick each box as the corresponding step is completed and approved.

After the issue exists, record its number for the rest of this runbook:

```bash
ISSUE_NUMBER=123
RELEASE_BRANCH="chore/${ISSUE_NUMBER}-prepare-${RELEASE_VERSION}-release"
```

### Confirm the release scope

- Confirm that all intended work is merged and no known release blockers remain.
- Choose the stable version according to the project's compatibility and
  semantic-versioning policy.
- Confirm that the stable version is valid under PEP 440.
- Review all changes since `PREVIOUS_TAG`, including dependency, security,
  documentation, and compatibility changes.
- Confirm that every new or changed public callable has the required stable
  `versionadded` or `versionchanged` directive.
- Confirm that the target version is not already present on PyPI or GitHub.
- Confirm that GitHub Actions, PyPI credentials, and GitHub authentication are
  available before beginning the release window.

Useful inspection commands include:

```bash
poetry --version
poetry version --short
git status --short --branch
git remote -v
git remote show origin
git fetch --prune origin
git fetch --tags origin
git log --oneline "${PREVIOUS_TAG}..origin/${PRIMARY_BRANCH}"
git diff --stat "${PREVIOUS_TAG}..origin/${PRIMARY_BRANCH}"
git tag --list "$RELEASE_TAG"
git ls-remote --tags origin "refs/tags/${RELEASE_TAG}"
gh auth status
```

The final two tag commands should produce no matching tag. Also check the PyPI
project's release history at `https://pypi.org/project/<project-name>/#history`.
The following request should return HTTP `404` for a version that has not been
published:

```bash
curl --fail --silent --show-error \
  "https://pypi.org/pypi/${PYPI_PROJECT}/${RELEASE_VERSION}/json" \
  > /dev/null
```

An exit status of `0` means the version already exists and must not be reused.
Only a confirmed HTTP `404` establishes absence. Curl status `22` alone can
represent other HTTP errors; network, authentication, and server failures remain
unresolved and block publication.

### Start from the current primary branch

Follow the repository's issue, branch, and pull-request policy. With the
**Maintainer Release** tracking issue from above already open, branch from
`main` using its issue number:

```bash
git switch "$PRIMARY_BRANCH"
git pull --ff-only origin "$PRIMARY_BRANCH"
git switch -c "$RELEASE_BRANCH"
poetry install --with dev --no-interaction --no-ansi
```

Do not include unrelated work in the release-preparation branch.

## 2. Promote the version to stable

Use Poetry to write the exact stable version back to `pyproject.toml`:

```bash
poetry version "$RELEASE_VERSION"
poetry version --short
git diff -- pyproject.toml poetry.lock
```

For example, the resulting project metadata should change as follows:

```toml
[project]
name = "pydplus"
version = "2.0.1"
```

Do not leave `.devN`, `aN`, `bN`, `rcN`, `.postN`, or a local `+label` suffix on
a normal stable release. Do not rely on the tag alone to supply the version
unless the repository deliberately uses a dynamic-versioning system.

### Handle `poetry.lock` deliberately

A project-only version change normally does not require dependency resolution.
Never edit `poetry.lock` by hand, and do not run `poetry update` merely because a
release is being prepared.

Validate the existing lock file:

```bash
poetry check --lock --strict
```

If dependency constraints or supported Python versions also changed, regenerate
the lock data with Poetry and review the entire diff:

```bash
poetry lock
poetry check --lock --strict
git diff -- pyproject.toml poetry.lock
```

`poetry lock` preserves already locked package versions when possible. Use
`poetry lock --regenerate` or `poetry update --lock` only when intentionally
refreshing all compatible dependency versions as separately reviewed release
work.

## 3. Finalize the changelog

Edit `docs/CHANGELOG.md` according to Keep a Changelog conventions.

### Preserve an empty Unreleased skeleton

Keep the `Unreleased` heading and each category already used by the project.
Move—not copy—the release bullets into a new versioned section. Replace each
moved category with an explicit placeholder so it is obvious that the section
was intentionally reset.

PyDPlus uses MyST target labels. Rename the labels moved into the release
section so every label remains unique. A representative transformation is:

```markdown
(relnotes-unreleased)=
## [Unreleased]

(unreleased-added)=
### Added

No unreleased additions at this time.

(unreleased-changed)=
### Changed

No unreleased changes at this time.

(unreleased-security)=
### Security

No unreleased security updates at this time.

---
(relnotes-2.0.1)=
## [2.0.1] - 2026-09-12

Summarize the release's purpose and most important compatibility information.

(relnotes-2.0.1-added)=
### Added

- Move the prior unreleased additions here.

(relnotes-2.0.1-changed)=
### Changed

- Move the prior unreleased changes here.

(relnotes-2.0.1-security)=
### Security

- Move the prior unreleased security notes here.
```

Use only the categories relevant to the repository's current changelog. Typical
Keep a Changelog categories are `Added`, `Changed`, `Deprecated`, `Removed`,
`Fixed`, and `Security`.

### Review the release notes as a reader

- Use the actual release date in `YYYY-MM-DD` form.
- Add a short release summary before the category headings when it helps.
- Preserve version qualifiers, compatibility warnings, CVE or advisory IDs,
  and migration instructions.
- Make the notes understandable without reading commits or pull requests.
- Remove duplicate, superseded, internal-only, and speculative wording.
- Verify that every bullet belongs to this release and that no unreleased bullet
  was accidentally left behind.
- Keep MyST roles and Markdown links valid; use single backticks for inline code
  in Markdown.

### Update changelog comparison links

At the bottom of `docs/CHANGELOG.md`, change the `Unreleased` comparison to start
at the new tag and add the new release comparison:

```markdown
[Unreleased]: https://github.com/jeffshurtliff/pydplus/compare/2.0.1...HEAD
[2.0.1]: https://github.com/jeffshurtliff/pydplus/compare/2.0.0...2.0.1
[2.0.0]: https://github.com/jeffshurtliff/pydplus/compare/1.0.1...2.0.0
```

Match the repository's tag convention exactly. If tags include a `v` prefix,
the comparison URLs must use `v2.0.1` even if the changelog heading is `2.0.1`.

## 4. Review other version-sensitive content

The package version and changelog are always required. The following files need
changes only when their current content becomes inaccurate:

- `README.md` installation, compatibility, status, or upgrade notices;
- `docs/getting-started/` and `docs/guides/` compatibility or migration text;
- API docstrings containing stable `versionadded`, `versionchanged`, or
  deprecation directives;
- `.readthedocs.yaml` and documentation version settings;
- Python-version classifiers and `requires-python` in `pyproject.toml`;
- support matrices in `.github/workflows/ci.yml`;
- package-level version constants when the repository does not use metadata as
  its single version source; and
- issue templates, examples, or badges that name the prior development version.

Search before deciding that no other edits are needed:

```bash
rg -n \
  "${PREVIOUS_TAG}|${RELEASE_VERSION}\.dev|will require|pre-release|prerelease" \
  README.md docs/getting-started docs/guides docs/reference docs/maintainers \
  docs/index.md docs/CHANGELOG.md .github/workflows .github/ISSUE_TEMPLATE \
  pyproject.toml requirements.txt src/pydplus tests
```

Do not mechanically replace historical release notes or old version directives.
Historical references should remain accurate.

## 5. Validate the preparation branch

Run the repository's complete pre-submit suite. For PyDPlus:

```bash
poetry check --lock --strict
poetry run ruff check .
poetry run ruff format --check .
poetry run pytest -q
poetry run bandit -r src
poetry run sphinx-build -W --keep-going -E -a -b html docs docs/_build/html
git diff --check
```

The `-E -a` options discard Sphinx's cached environment and rebuild every page.
Open the rendered index and confirm that its displayed package version is the
stable release version rather than an older cached or installed version.

If the rendered version is stale, compare Poetry's active metadata with ignored
build metadata before changing source files:

```bash
poetry version --short
poetry run python -c \
  "from importlib.metadata import version; print(version('${PYPI_PROJECT}'))"
find src -maxdepth 2 -type d -name '*.egg-info' -print
```

An old generated `src/*.egg-info/` directory can shadow current metadata during
the docs build. Do not edit generated metadata by hand. After confirming that a
directory is ignored, stale, and safe to discard, remove it, reinstall the
project with Poetry, and repeat the clean Sphinx build.

Integration validation is recommended when an authorized ID Plus test environment
is available. It is not a mandatory release prerequisite when access is not
feasible. Run `poetry run pytest --run-integration tests/integration -q` with the
appropriate environment; appropriately mocked integration checks may also be
run. Record real-environment results, mocked results, or a skipped status with
the reason in the release report. A skip due to unavailable environment access
does not block release readiness. Investigate failures from checks that are run
before declaring readiness.

Do not open `local/`, `.env`, or encrypted/decrypted helper files to establish
environment availability. Use `examples/helper_example.json` for placeholder
configuration references. Never expose credentials in command output, logs,
release notes, artifacts, or commits.

### Build and inspect candidate artifacts

Build both the source distribution and wheel, then make Twine treat rendering
warnings as failures:

```bash
RELEASE_DIST_DIR=$(mktemp -d)
poetry build --output "$RELEASE_DIST_DIR"
poetry run twine check --strict "$RELEASE_DIST_DIR"/*.whl "$RELEASE_DIST_DIR"/*.tar.gz
ls -lh "$RELEASE_DIST_DIR"
tar -tzf "$RELEASE_DIST_DIR"/*.tar.gz
unzip -l "$RELEASE_DIST_DIR"/*.whl
poetry run python .agents/skills/pydplus-stable-release-prep/scripts/inspect_release_artifacts.py \
  --dist-dir "$RELEASE_DIST_DIR" --expected-version "$RELEASE_VERSION" --strict
```

Confirm that:

- exactly one expected source distribution and the expected wheel or wheels were
  created;
- every filename contains the stable release version;
- package metadata names the correct project and stable version;
- the source distribution contains the intended source, `pyproject.toml`, README,
  and license files;
- the wheel contains package code and metadata but no tests, secrets, local
  configuration, caches, or unrelated generated files; and
- `twine check --strict` passes for every artifact.

### Smoke-test the wheel in clean environments

Use the distribution name, not necessarily the import name, for the metadata
assertion. First install the wheel without dependencies so the metadata check is
isolated from dependency resolution:

```bash
RELEASE_METADATA_SMOKE_DIR=$(mktemp -d)
poetry run python -m venv "$RELEASE_METADATA_SMOKE_DIR"
"$RELEASE_METADATA_SMOKE_DIR/bin/python" -m pip install --no-deps "$RELEASE_DIST_DIR"/*.whl
"$RELEASE_METADATA_SMOKE_DIR/bin/python" -c \
  "from importlib.metadata import version; assert version('${PYPI_PROJECT}') == '${RELEASE_VERSION}'"
```

Use a second clean environment for the public-API smoke test. Import the client only; do not instantiate it or
connect to a tenant during package smoke tests. Install the wheel
normally so its declared runtime dependencies are present:

```bash
RELEASE_IMPORT_SMOKE_DIR=$(mktemp -d)
poetry run python -m venv "$RELEASE_IMPORT_SMOKE_DIR"
"$RELEASE_IMPORT_SMOKE_DIR/bin/python" -m pip install "$RELEASE_DIST_DIR"/*.whl
"$RELEASE_IMPORT_SMOKE_DIR/bin/python" -c \
  "from pydplus import PyDPlus; assert PyDPlus is not None"
```

Adapt the final import or functional check to the package's public API. Do not
require a package import in the `--no-deps` environment when importing the
package legitimately requires declared runtime dependencies. CI should cover
every supported Python version; these local smoke tests are additional artifact
checks, not substitutes for CI.

### Review the complete diff

```bash
git status --short
git diff --stat
git diff
```

Keep candidate archives in `RELEASE_DIST_DIR`. Confirm that generated
`dist/` and `docs/_build/` content remains ignored and unstaged. Confirm that only deliberate release-preparation files changed.

## 6. Commit, review, merge, and push the preparation

Stage only the intended files and use a focused, past-tense commit message:

```bash
git add pyproject.toml docs/CHANGELOG.md
# Add any other intentionally updated release files explicitly.
git diff --cached --check
git diff --cached
git commit -m "Prepared ${PYPI_PROJECT} ${RELEASE_VERSION} release (#${ISSUE_NUMBER})"
git push -u origin "$RELEASE_BRANCH"
```

Open a pull request that references the release issue and follows the repository's
template and labeling policy. With GitHub CLI, the starting point is:

```bash
gh pr create \
  --base "$PRIMARY_BRANCH" \
  --head "$RELEASE_BRANCH" \
  --title "Prepared ${PYPI_PROJECT} ${RELEASE_VERSION} release" \
  --label chore --label maintainer --label codex \
  --body "Prepares the ${RELEASE_VERSION} release. Closes #${ISSUE_NUMBER}."
```

Review and merge the pull request using the repository's normal merge strategy.
The merge updates `origin/$PRIMARY_BRANCH`; do not tag the release-branch commit.

For the normal pull-request path, synchronize the merged primary branch locally:

```bash
git switch "$PRIMARY_BRANCH"
git pull --ff-only origin "$PRIMARY_BRANCH"
git status --short --branch
test "$(git rev-parse HEAD)" = "$(git rev-parse "origin/${PRIMARY_BRANCH}")"
```

Wait for every required GitHub check on this exact commit to succeed. Useful
GitHub CLI commands are:

```bash
RELEASE_COMMIT=$(git rev-parse HEAD)
gh run list --commit "$RELEASE_COMMIT" --limit 10
gh run watch RUN_ID --exit-status
```

Replace `RUN_ID` with each required run identifier. Do not tag a commit with
failed, cancelled, skipped-required, or still-running checks.

## 7. Rebuild from the exact release commit

This is the final approval checkpoint before external release state is created.
Confirm explicit authorization for the remaining actions.

Start with the clean, synchronized primary branch and rebuild. Never reuse the
candidate archives built before the merge:

```bash
git status --short --branch
test -z "$(git status --porcelain)"
test "$(git rev-parse HEAD)" = "$(git rev-parse "origin/${PRIMARY_BRANCH}")"
poetry version --short
poetry check --lock --strict
RELEASE_DIST_DIR=$(mktemp -d)
poetry build --output "$RELEASE_DIST_DIR"
poetry run twine check --strict "$RELEASE_DIST_DIR"/*.whl "$RELEASE_DIST_DIR"/*.tar.gz
shasum -a 256 "$RELEASE_DIST_DIR"/*.whl "$RELEASE_DIST_DIR"/*.tar.gz > "$RELEASE_DIST_DIR"/SHA256SUMS
cat "$RELEASE_DIST_DIR"/SHA256SUMS
```

Repeat the artifact inspection and clean-environment smoke test from the previous
phase. Record the release commit and checksums in the release notes or release
work log.

## 8. Create and push the annotated release tag

PyDPlus uses bare, annotated version tags. Create the tag on the verified
primary-branch commit:

```bash
git tag -a "$RELEASE_TAG" -m "${PYPI_PROJECT} ${RELEASE_VERSION}"
git show --no-patch --format=fuller "$RELEASE_TAG"
test "$(git rev-list -n 1 "$RELEASE_TAG")" = "$(git rev-parse HEAD)"
git push origin "$RELEASE_TAG"
git ls-remote --tags origin "refs/tags/${RELEASE_TAG}"
```

Push only the intended tag; avoid `git push --tags`. If the repository requires
signed tags and the signing key is configured, use `git tag -s` instead of
`git tag -a`.

Do not move or reuse a published release tag. If the tag points to the wrong
commit, stop before uploading to PyPI and resolve the incident deliberately.

## 9. Create a draft GitHub Release

Prepare concise GitHub release notes from the new changelog section. Include the
summary, user-relevant category bullets, compatibility or migration warnings,
and a link to the full changelog. Do not paste MyST target labels into the
GitHub body.

Create a draft from the already-pushed tag and attach the exact verified
artifacts plus their checksums:

```bash
gh release create "$RELEASE_TAG" \
  "$RELEASE_DIST_DIR"/*.whl "$RELEASE_DIST_DIR"/*.tar.gz "$RELEASE_DIST_DIR"/SHA256SUMS \
  --repo "$GITHUB_REPOSITORY" \
  --draft \
  --verify-tag \
  --fail-on-no-commits \
  --title "${PYPI_PROJECT} ${RELEASE_VERSION}" \
  --notes-file -
```

Paste the prepared release notes, then send end-of-file with `Ctrl-D`. Review the
draft and its assets before continuing:

```bash
gh release view "$RELEASE_TAG" \
  --repo "$GITHUB_REPOSITORY" \
  --json tagName,isDraft,isPrerelease,assets,url
```

The release must still be a draft, must not be marked as a prerelease, and must
reference the intended tag and assets.

## 10. Upload the distributions to PyPI

> **Irreversible step:** Reconfirm the project name, version, filenames,
> checksums, tag, release commit, and production repository before continuing.

Use a project-scoped PyPI API token where possible. When prompted for token-based
credentials, the username is `__token__` and the password is the complete token,
including its `pypi-` prefix. Do not put a token in a command, tracked file,
terminal transcript, issue, pull request, or release notes.

For future CI-based release automation, prefer PyPI Trusted Publishing over a
stored, long-lived API token. This manual runbook uses Twine because it keeps the
final production action under direct maintainer control.

Upload only the wheel and source distribution—not the checksum file—to the
production `pypi` repository:

```bash
poetry run twine upload --repository pypi "$RELEASE_DIST_DIR"/*.whl "$RELEASE_DIST_DIR"/*.tar.gz
```

Confirm that Twine reports the production PyPI upload endpoint and a successful
upload for every expected file. Do not use `--skip-existing` in the normal
release process because it can hide an accidental duplicate or partial release.

### Optional TestPyPI rehearsal

TestPyPI is useful for a new packaging configuration, but it is a separate index
with separate credentials and incomplete dependency coverage. Use it before the
production command and install with `--no-deps`:

```bash
poetry run twine upload --repository testpypi "$RELEASE_DIST_DIR"/*.whl "$RELEASE_DIST_DIR"/*.tar.gz
TESTPYPI_SMOKE_DIR=$(mktemp -d)
poetry run python -m venv "$TESTPYPI_SMOKE_DIR"
"$TESTPYPI_SMOKE_DIR/bin/python" -m pip install \
  --index-url https://test.pypi.org/simple/ \
  --no-deps \
  "${PYPI_PROJECT}==${RELEASE_VERSION}"
```

TestPyPI uploads also create external state and require explicit authorization.

## 11. Verify the production PyPI release

Open `https://pypi.org/project/<project-name>/<version>/` and confirm:

- the version, description, README rendering, license, project URLs, classifiers,
  and Python requirement are correct;
- all expected distribution files and no unexpected files are present; and
- PyPI's hashes match `"$RELEASE_DIST_DIR"/SHA256SUMS`.

Install the release from PyPI into a new environment without using the local
wheel or pip cache:

```bash
PYPI_SMOKE_DIR=$(mktemp -d)
poetry run python -m venv "$PYPI_SMOKE_DIR"
"$PYPI_SMOKE_DIR/bin/python" -m pip install \
  --no-cache-dir \
  "${PYPI_PROJECT}==${RELEASE_VERSION}"
"$PYPI_SMOKE_DIR/bin/python" -c \
  "from importlib.metadata import version; assert version('${PYPI_PROJECT}') == '${RELEASE_VERSION}'"
```

Run the same minimal public-API smoke test used for the local artifact.

## 12. Publish and verify the GitHub Release

After the PyPI page and clean installation are correct, publish the existing
draft and mark the stable release as latest:

```bash
gh release edit "$RELEASE_TAG" \
  --repo "$GITHUB_REPOSITORY" \
  --draft=false \
  --latest
gh release view "$RELEASE_TAG" \
  --repo "$GITHUB_REPOSITORY" \
  --json tagName,isDraft,isPrerelease,url,assets
```

Confirm in GitHub that:

- the release is published rather than draft or prerelease;
- the tag points to the verified release commit;
- the title and release notes are accurate;
- the wheel, source distribution, and checksum file are attached; and
- the release is marked `Latest` when appropriate.

## 13. Complete post-release work

- Verify that the GitHub tag, GitHub Release, PyPI project, and package metadata
  all show the same version.
- Verify that the `stable` documentation build points to the new release and that
  `latest` remains coherent for ongoing development.
- Close the release issue or milestone and record any follow-up work.
- With explicit authorization to send announcements, announce the release through the project's normal channels.
- Retain the release commit and artifact checksums in the release record.
- Start the next development cycle in a separate branch and pull request.

For the next development cycle, choose the intended next patch or minor version
rather than guessing it. For example:

```bash
NEXT_DEV_VERSION=2.0.2.dev0
poetry version "$NEXT_DEV_VERSION"
poetry check --lock --strict
git diff -- pyproject.toml docs/CHANGELOG.md poetry.lock
```

The changelog's `Unreleased` skeleton should already be empty and ready for new
entries. Commit and merge the next-development-version change according to the
repository's normal workflow; do not fold it into the already tagged release.

## Failure and recovery guidance

### Before pushing the tag

Fix the release branch or primary branch normally, rerun all checks, rebuild, and
create the tag only after the corrected commit is merged. A local tag that has
not been pushed can be deleted and recreated after confirming its exact name:

```bash
git tag --delete "$RELEASE_TAG"
```

### After pushing the tag but before PyPI upload

Stop. Do not silently move a public tag. Determine whether the draft release or
tag has been consumed, whether repository immutability is enabled, and whether a
new patch version is safer. Document the decision.

### During a partial PyPI upload

Stop automatic retries after a failed or uncertain upload. Verify remote state
and report accepted and missing files before any specifically authorized retry.

Record exactly which unchanged files PyPI accepted. Do not rebuild them. After
comparing local and PyPI hashes, upload only an unchanged missing artifact if it
is valid and safe to do so. If an incorrect artifact or metadata was published,
prepare a new patch release; deleting a PyPI file does not make its filename
reusable.

### After PyPI publication

Never overwrite, reuse, or retag the published version. Correct problems with a
new release, yank the affected release on PyPI when appropriate, and publish a
clear advisory or changelog note.

## Definition of done

- [ ] A **Maintainer Release** tracking issue recorded the release, and each
  publication authorization was granted and checked off on it.
- [ ] Stable version is present in every authoritative version source.
- [ ] `Unreleased` is empty but retains its category skeleton and placeholders.
- [ ] The new dated changelog section and comparison links are correct.
- [ ] Poetry validation, lint, formatting, tests, docs, and CI all pass.
- [ ] Wheel and source distribution pass strict Twine validation and smoke tests.
- [ ] Primary branch, annotated tag, GitHub Release, and PyPI use the same commit
  and version.
- [ ] PyPI installation succeeds in a clean environment.
- [ ] GitHub Release is published with verified artifacts and checksums.
- [ ] Stable documentation and project tracking are updated.
- [ ] The next `.dev0` cycle is started separately when appropriate.

## Official references

- [Poetry command reference](https://python-poetry.org/docs/cli/)
- [Python Packaging User Guide: Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [Python Packaging User Guide: Tool Recommendations](https://packaging.python.org/en/latest/guides/tool-recommendations/)
- [Twine documentation](https://twine.readthedocs.io/en/stable/)
- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
- [GitHub CLI: `gh release create`](https://cli.github.com/manual/gh_release_create)
- [GitHub CLI: `gh release edit`](https://cli.github.com/manual/gh_release_edit)
- [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
- [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
