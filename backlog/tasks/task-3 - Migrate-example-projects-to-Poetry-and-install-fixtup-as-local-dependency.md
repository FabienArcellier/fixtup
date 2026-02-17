---
id: TASK-3
title: Migrate example projects to Poetry and install fixtup as local dependency
status: To Do
assignee: []
created_date: '2026-02-17 09:28'
labels:
  - examples
  - poetry
  - dependencies
dependencies: []
priority: medium
---

## Description
<!-- SECTION:DESCRIPTION:BEGIN -->
Migrate the example projects located in ./examples from their current setup to Poetry. Update the dependency management so that fixtup is installed as a local dependency (using path-based installation) rather than being pulled from PyPI.

This will make it easier to test changes to fixtup against the examples without needing to publish to PyPI first.

### Impacts

#### Positive
- Easier local development and testing of fixtup changes
- No need to publish to PyPI to test examples
- Consistent dependency management across all projects

#### Negative
- Requires updating all example project configurations
- Contributors need Poetry installed to run examples

#### Further consideration
- Consider adding a script to automate the migration process
- Document the new setup process for contributors

<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] Migrate all example projects in ./examples to use Poetry
- [ ] Configure fixtup as a local path dependency instead of PyPI
- [ ] Verify examples still work after migration
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->

### Files

- examples/*/pyproject.toml (new files for each example)
- examples/*/requirements.txt (to be removed)
- examples/*/setup.py (to be removed if exists)

<!-- SECTION:PLAN:END -->
