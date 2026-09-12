Maintainers
===========

Use this section for project-maintenance procedures that are performed by the
repository's maintainers rather than by contributors submitting changes.

These guides are designed to provide repeatable, safety-conscious workflows for
tasks that can change published packages, repository history, tags, releases,
or other external project state.

Recommended starting point:

1. Use :doc:`releasing` when promoting a development version to a stable release
   and publishing it to PyPI and GitHub.
2. Use :doc:`stable-release-prep-skill` when an agent will perform the reversible
   preparation and validation work before the publication checkpoints.

Before beginning a maintainer procedure, confirm that you have:

- Reviewed the repository's current ``AGENTS.md`` and ``CONTRIBUTING.md`` files
- Identified the correct issue, branch, version, and release scope
- Verified the required credentials and external-service access
- Distinguished reversible preparation from actions that require explicit
  publication approval

For contributor-facing development and pull-request requirements, see the
repository's ``CONTRIBUTING.md`` file. For published release history, see the
:doc:`../CHANGELOG`.

.. toctree::
   :maxdepth: 1
   :hidden:

   releasing
   stable-release-prep-skill
