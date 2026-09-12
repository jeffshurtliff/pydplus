(maintainer-stable-release-prep-skill)=
# Using the PyDPlus Stable Release Prep Skill

The repository includes an agent skill for preparing a development or prerelease
version of PyDPlus as a stable release candidate. The skill coordinates the
reversible preparation and validation work in the {doc}`releasing` runbook while
preserving the runbook's approval boundaries for repository history and external
publication.

The skill is stored at:

```text
.agents/skills/pydplus-stable-release-prep/
```

Invoke the repository skill by name in a compatible agent, or direct the agent
to read its `SKILL.md` file explicitly. No user-level skill installation is required.

Claude Code discovers repository skills under `.claude/skills/`. Rather than
maintaining a second copy there, the repository provides `.claude/skills/pydplus-stable-release-prep`
as a symlink to the canonical `.agents/skills/pydplus-stable-release-prep/` directory, so both agent
families read the same `SKILL.md` and stay in sync automatically.

It is repository-owned and contains no credentials, private helper data, local
filesystem paths, or maintainer-specific environment configuration.

## When to use the skill

Use the skill when promoting the static version in `pyproject.toml` from a
development or prerelease value, such as `2.0.1.dev0`, to its intended stable
version, such as `2.0.1`.

Do not use it for routine dependency updates, ordinary development-version
bumps, prerelease publication, or projects outside the PyDPlus repository.

The runbook remains authoritative. Read {doc}`releasing` before beginning a
release window, particularly when continuing beyond local preparation.

## Prerequisites

Before invocation, confirm that:

- the repository is available in a clean working tree;
- the intended release work has been merged into `main`;
- a **Maintainer Release** tracking issue
  (`.github/ISSUE_TEMPLATE/maintainer-release.md`) has been opened and the exact
  stable version has been identified;
- Poetry and the project's development dependencies are installed; and
- read-only access to GitHub and PyPI is available for duplicate-version checks.

Credentials for later publication must remain outside the repository and must
never be pasted into an agent prompt, command, issue, pull request, artifact, or
release note.

## Invoke the skill

From a compatible agent working at the repository root, invoke the skill by its
name and provide the target version and issue number:

```text
Use $pydplus-stable-release-prep to prepare PyDPlus 2.0.1 from
2.0.1.dev0 using issue #123. Complete all local preparation and validation,
then stop before staging, committing, pushing, tagging, or publishing anything.
```

Replace the example values with the approved release values. Supplying the
previous stable tag is optional when it can be established unambiguously from
reachable Git history and the changelog.

Agents that do not automatically discover repository skills can be directed to
read `.agents/skills/pydplus-stable-release-prep/SKILL.md` before performing
the same request.

## Default scope

The preparation request authorizes the skill to:

- perform local and read-only remote preflight checks;
- create or use the policy-compliant local release branch;
- promote the Poetry version and finalize the changelog;
- update version-sensitive maintained documentation when needed;
- run lint, formatting, test, documentation, build, and artifact checks;
- smoke-test the built wheel in clean temporary virtual environments; and
- report candidate artifact names and SHA-256 checksums.

The preparation request does **not** authorize the skill to:

- create or modify a GitHub issue or pull request;
- stage, commit, merge, or push changes;
- create or push a tag;
- upload to TestPyPI or PyPI; or
- create, edit, publish, or delete a GitHub Release.

Each later action requires explicit authorization. Approval for one action does
not imply approval for the next.

## Expected result

On successful completion, the skill returns a release-readiness report with:

- the resolved version, date, tags, branch, and release scope;
- the files changed and the reason for each change;
- pass, fail, or skipped status for every required check;
- the candidate source distribution and wheel checksums;
- any unresolved blocker or manual review; and
- the next action that requires maintainer authorization.

The working tree should contain only deliberate release-preparation changes.
Candidate distributions stay in their temporary build directory; Sphinx output
must remain ignored and unstaged. Integration validation is recommended when
an authorized ID Plus test environment is available, but is optional when access
is not feasible. Report whether it ran against a real or mocked environment, or
was skipped and why. A skip due to unavailable environment access does not block
release readiness; failures from checks that are run must still be investigated.

## Continue after preparation

After reviewing the local changes, authorize later actions separately and name
their exact scope. For example:

```text
Using $pydplus-stable-release-prep, stage and commit only the validated
release-preparation files for issue #123. Do not push the branch.
```

A later request may authorize pushing the branch and creating a pull request.
Tagging, TestPyPI, production PyPI, and GitHub Release operations remain separate
checkpoints. Before each action, the agent must reread the corresponding section
of {doc}`releasing` and revalidate its prerequisites.

Candidate archives built before the preparation pull request is merged must
never be reused for publication. Publication artifacts must be rebuilt from the
exact, synchronized, CI-verified commit on `main`.

## Artifact inspector

The skill includes a deterministic archive inspector. After the runbook creates `RELEASE_DIST_DIR` and builds the candidate there, it can be run directly from the repository root:

```bash
poetry run python .agents/skills/pydplus-stable-release-prep/scripts/inspect_release_artifacts.py \
  --dist-dir "$RELEASE_DIST_DIR" \
  --expected-version "2.0.1" \
  --strict
```

The inspector verifies the PyDPlus distribution name and version, required
source files, wheel metadata, expected archive counts, suspicious secret or local
configuration paths, package code, and SHA-256 checksums. Strict mode treats
suspicious archive warnings as failures.

This check supplements `poetry run twine check --strict`; it does not replace
Twine, clean-environment installation, CI, or manual release review.

The release workflow uses separate environments for wheel smoke tests. The
first installs with `--no-deps` and validates distribution metadata. The second
installs the wheel normally with its runtime dependencies before importing the
public `PyDPlus` client. A dependency-free environment is not expected to
import the client successfully.

## Maintaining the skill

When the release workflow changes, update these sources together:

- `.agents/skills/pydplus-stable-release-prep/SKILL.md`;
- the included artifact inspector when archive rules change;
- `.github/ISSUE_TEMPLATE/maintainer-release.md` when the release phases or
  authorization checkpoints change;
- {doc}`releasing`; and
- this usage guide.

`.claude/skills/pydplus-stable-release-prep` is a symlink to the canonical
`.agents/skills/pydplus-stable-release-prep/` directory, not a separate copy, so it
requires no maintenance of its own; confirm the symlink still resolves after any
repository restructuring.

Validate the skill structure with the agent platform's skill validator when one
is available. Always run Ruff against the Python helper, build the Sphinx
documentation with warnings treated as errors, and exercise the inspector
against both valid and deliberately invalid temporary artifacts.
