---
id: TASK-2
title: Move the project from setup.cfg to poetry 2.0
status: Done
assignee: []
created_date: '2026-02-16 23:38'
updated_date: '2026-02-17 08:29'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Migrate the fixtup project build system from setuptools (setup.cfg) to Poetry 2.0 to leverage modern Python packaging standards, deterministic dependency resolution with lock files, and improved developer tooling.

### Impacts

#### Positive

- **Deterministic builds**: Poetry generates a poetry.lock file ensuring reproducible builds across all environments
- **Modern dependency management**: Superior dependency resolution with conflict detection and automatic virtual environment management
- **Simplified publishing**: Built-in `poetry publish` command streamlines PyPI releases without twine
- **Unified configuration**: Single pyproject.toml file replaces setup.cfg, requirements files, and MANIFEST.in
- **Enhanced developer experience**: Intuitive CLI commands (`poetry add`, `poetry update`, `poetry shell`)
- **Better CI/CD integration**: Poetry supports caching and has official GitHub Actions support
- **Improved security**: Poetry.lock enables vulnerability scanning and audit capabilities

#### Negative

- **Learning curve**: Team members unfamiliar with Poetry need time to adapt
- **Migration effort**: Converting setup.cfg metadata, entry points, and package data requires careful attention
- **Tool compatibility**: Some existing tools may need configuration updates (mypy, alfred-cli)
- **Virtual environment shift**: Developers must adapt to Poetry's venv management approach

#### Further consideration

- Evaluate Poetry 2.0 specific features (PEP 621 compliance, new lock file format)
- Assess impact on Windows/macOS CI workflows using pipenv
- Plan migration strategy for example projects with their own setup.cfg
- Consider maintaining backward compatibility during transition period
- Review mypy configuration currently in setup.cfg section [mypy]
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Create pyproject.toml with Poetry 2.0 configuration matching current setup.cfg metadata
- [x] #2 Migrate all dependencies from setup.cfg [options] and [options.extras_require] to pyproject.toml
- [x] #3 Convert entry points (console_scripts) to Poetry scripts configuration
- [x] #4 Ensure package data and resources are properly included in Poetry build
- [x] #5 Update alfred/ commands to use poetry instead of pipenv
- [x] #6 Migrate mypy configuration from setup.cfg to pyproject.toml or separate config
- [x] #7 Update GitHub Actions workflows (ci.yml, ci-macos.yml, ci-windows.yml) to use Poetry
- [x] #8 Update publish.yml workflow to use poetry publish
- [ ] #9 Verify all example projects still work or update their documentation
- [x] #10 Update README.md with Poetry installation and usage instructions
- [x] #11 Remove setup.cfg after successful migration
- [x] #12 Ensure CI passes on Python 3.10, 3.11, 3.12, 3.13, 3.14
- [x] #13 Fix les versions de toutes les dépendances
- [x] #14 Migrate windows dependency in poetry section [tool.poetry.group.dev_windows.dependencies]
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
### Steps

1. **Analyze current setup**
   - Document all metadata, dependencies, and configurations in setup.cfg
   - Review alfred commands that use pipenv
   - Identify mypy and other tool configurations

2. **Create pyproject.toml**
   - Initialize Poetry project with `poetry init`
   - Add project metadata (name, version, description, authors, license, etc.)
   - Configure packages and package data
   - Add all runtime dependencies
   - Add dev dependencies (mypy, sphinx, etc.)
   - Configure console scripts entry point

3. **Update alfred commands**
   - Modify alfred/ci.py to use poetry run instead of pipenv run
   - Update alfred/tests.py, alfred/lint.py, alfred/docs.py
   - Update alfred/publish.py to use poetry publish

4. **Update CI/CD workflows**
   - Install poetry with pip (do not use GitHub Actions module)
   - Update commands from `pipenv run` to `poetry run`
   - Disable caching

5. **Migrate tool configurations**
   - Move [mypy] section from setup.cfg to pyproject.toml [tool.mypy]
   - Verify other tool configurations

6. **Testing and validation**
   - Run full test suite locally with Poetry
   - Verify CI passes on all Python versions
   - Test publishing workflow (dry-run)
   - Validate example projects

7. **Documentation update**
   - Update README.md installation instructions
   - Update AGENTS.md if needed
   - Document Poetry commands for contributors

8. **Cleanup**
   - Remove setup.cfg
   - Remove Pipfile and Pipfile.lock
   - Update .gitignore if needed

9. **Migrate windows dependency**
   - Create [tool.poetry.group.dev_windows.dependencies] section
   - Remove [project.optional-dependencies] section
   - Update poetry.lock

### Files

- setup.cfg (source of migration)
- pyproject.toml (target configuration)
- alfred/ci.py
- alfred/tests.py
- alfred/lint.py
- alfred/docs.py
- alfred/publish.py
- alfred/dist.py
- .github/workflows/ci.yml
- .github/workflows/ci-macos.yml
- .github/workflows/ci-windows.yml
- .github/workflows/publish.yml
- .github/workflows/validate_examples.yml
<!-- SECTION:PLAN:END -->
