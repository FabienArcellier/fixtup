---
id: TASK-2
title: Move the project from setup.cfg to poetry 2.0
status: To Do
assignee: []
created_date: '2026-02-16 23:38'
labels: []
dependencies: []
---

## Description
<!-- SECTION:DESCRIPTION:BEGIN -->
Migrate the project build system from setup.cfg to Poetry 2.0 for better dependency management and modern Python packaging.

### Impacts

#### Positive
- Modern dependency management with lock file
- Better virtual environment handling
- Simplified publishing to PyPI
- Improved developer experience with poetry commands

#### Negative
- Learning curve for developers not familiar with Poetry
- Migration effort required to convert existing setup

#### Further consideration
- Evaluate if all current setup.cfg features are supported by Poetry
- Check compatibility with existing CI/CD pipeline
- Consider migration path for existing pipenv users

<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] Migrate setup.cfg configuration to pyproject.toml
- [ ] Update build commands in alfred/ to use poetry
- [ ] Ensure all dependencies are properly declared in pyproject.toml
- [ ] Verify CI/CD pipeline works with Poetry
- [ ] Update documentation for Poetry usage
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->

### Files
- setup.cfg
- pyproject.toml
- alfred/
- .github/workflows/
- README.md
- examples/*/setup.cfg

<!-- SECTION:PLAN:END -->
