# CLAUDE.md

`AGENTS.md` is the canonical contributor guide for this repository. **Read it
first and follow it in full** — every rule in it applies to Claude Code. This
file adds only the notes that are specific to working here with Claude Code.

Keep it that way: if a rule applies to every agent or contributor, put it in
`AGENTS.md`, not here. This file should stay short and never contradict
`AGENTS.md`.

## Environment and commands

- Dependency management and builds use **Poetry** (see `AGENTS.md` →
  "Dev environment"). Supported Python: 3.12, 3.13, and 3.14.
- Before handing work back, run and report the same checks CI runs:
  - `poetry run ruff check .`
  - `poetry run ruff format --check .`
  - `poetry run pytest -q`
- Integration tests need a real (or mocked) helper/tenant configuration and are
  opt-in. Do not run `--run-integration` unless the user asks and a helper file
  is available.

## Header block attribution

When you change a file whose header block has `:Last Modified:` /
`:Modified Date:` fields, update them per `AGENTS.md` → "Documentation
expectations". For Claude Code specifically:

- `:Last Modified:` field → `<orchestrating person> (via <exact model id>)`,
  e.g. `Jeff Shurtliff (via claude-sonnet-5)`. Use the real model ID you are
  running as (for example `claude-sonnet-5`, `claude-opus-5`,
  `claude-haiku-4-5`), not a marketing name. If the person prefers not to be
  named, use `Anonymous (via <model id>)`.
- `:Modified Date:` field → today's local date, matching the existing format
  (`DD Mon YYYY`).
- Only touch these fields on files you actually changed.

## Secrets — never read, print, or commit

See `AGENTS.md` → "Secrets and local-only files". Treat these as off-limits:
`local/`, `.env`, and any real helper/config files with live RSA ID Plus
tenant credentials, private keys, or client secrets. Never open them, echo
their contents, paste them into code/docs/commit messages, or add real
credentials to any tracked file. Use `examples/helper_example.json`
(placeholder values only) as the reference.

## Git

- Work on a branch, never directly on `main`. Branch prefixes and the
  issue-number convention are in `CONTRIBUTING.md` (`feature/`, `fix/`,
  `refactor/`, `chore/`, `docs/`, `test/`, `ci/`, `security/`).
- Do not commit or push unless the user asks.
- Commit messages: past tense ("Updated the ...", "Added ..."), focused, and
  mention the file name when it reads naturally. The Claude Code harness
  appends the `Co-Authored-By:` and session trailers automatically — keep them.
- Update `docs/CHANGELOG.md` for any user-visible change.

## Working style for this repo

- Plan non-trivial changes before editing; this project values small,
  localized, well-tested diffs over broad refactors.
- Don't remove Python 3.12 support or widen/narrow the supported version range
  without explicit maintainer authorization (see `AGENTS.md` → "Python version
  support").
- `/code-review` before opening a PR catches the correctness and cleanup
  issues reviewers here look for.
- Follow the pre-submit checklist in `AGENTS.md` before wrapping up.
