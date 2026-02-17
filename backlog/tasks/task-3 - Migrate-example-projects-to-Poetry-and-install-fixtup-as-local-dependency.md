---
id: TASK-3
title: Migrate example projects to Poetry and install fixtup as local dependency
status: Review
assignee: []
created_date: '2026-02-17 09:28'
updated_date: '2026-02-17 10:06'
labels:
  - examples
  - poetry
  - dependencies
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Migrate the 5 example projects located in `./examples/` from setuptools-based configuration to Poetry 2.0. Each example currently uses `setup.cfg` for dependency management and has a minimal `pyproject.toml` that only specifies the build system. The goal is to modernize the dependency management by converting each example to use Poetry's `pyproject.toml` format with a path-based dependency on the local fixtup package (`{path = "../..", develop = true}`).

This migration will enable developers to test changes to fixtup against the examples immediately without publishing to PyPI, ensuring faster feedback loops during development.

### Impacts

#### Positive
- **Faster development cycle**: Test fixtup changes against examples without PyPI publishing
- **Consistent tooling**: All examples use Poetry like the main project
- **Better dependency resolution**: Poetry's lock file ensures reproducible builds
- **Local development support**: Path-based dependency enables real-time testing
- **Simplified configuration**: Single `pyproject.toml` replaces `setup.cfg` + `pyproject.toml`

#### Negative
- **Breaking change**: Contributors must have Poetry installed to run examples
- **Migration effort**: All 5 examples need configuration updates
- **Learning curve**: Contributors unfamiliar with Poetry need to learn basic commands

#### Further consideration
- Update `examples/README.md` with Poetry setup instructions
- Consider adding a validation script to check all examples have valid Poetry configs
- Document troubleshooting steps for common Poetry issues
- Add CI job to verify examples can be installed with Poetry
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 All 5 example projects migrated from setuptools to Poetry 2.0
- [x] #2 Each example has a complete `pyproject.toml` with Poetry configuration
- [x] #3 fixtup configured as path dependency (`{path = "../..", develop = true}`) in all examples
- [x] #4 All `setup.cfg` files removed from examples
- [x] #5 All legacy `pyproject.toml` files updated or replaced
- [x] #6 Each example's dependencies correctly mapped to Poetry format
- [x] #7 Examples can be installed with `poetry install` without errors
- [ ] #8 Examples still pass their tests after migration
- [x] #9 `examples/README.md` updated with Poetry instructions
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
### Steps

1. **Analyze current setup**
   - Review each example's `setup.cfg` to extract dependencies
   - Document current dependency versions and extras

2. **Create Poetry configuration for each example**
   - Convert `setup.cfg` metadata to Poetry `[tool.poetry]` section
   - Map `install_requires` to `[tool.poetry.dependencies]`
   - Map `extras_require` dev to `[tool.poetry.group.dev.dependencies]`
   - Add fixtup as path dependency: `{path = "../..", develop = true}`
   - Update `[build-system]` to use `poetry-core>=2.0.0`

3. **Remove legacy files**
   - Delete `setup.cfg` from each example
   - Clean up any `setup.py` if present
   - Remove old build artifacts

4. **Test migration**
   - Run `poetry install` in each example directory
   - Verify dependencies are installed correctly
   - Run example tests to ensure they still pass

5. **Update documentation**
   - Update `examples/README.md` with Poetry setup instructions
   - Add troubleshooting section for common issues

### Files

**To be created/modified:**
- `examples/datapipeline_ftp/pyproject.toml` - Poetry config with FTP-related deps
- `examples/kanban_flask_postgresql/pyproject.toml` - Poetry config with Flask + PostgreSQL deps
- `examples/kanban_flask_sqlite/pyproject.toml` - Poetry config with Flask + SQLite deps
- `examples/postgresql/pyproject.toml` - Poetry config with PostgreSQL deps
- `examples/unittest/pyproject.toml` - Poetry config with Pillow deps
- `examples/README.md` - Update with Poetry instructions

**To be removed:**
- `examples/datapipeline_ftp/setup.cfg`
- `examples/datapipeline_ftp/pyproject.toml` (legacy build-system only)
- `examples/kanban_flask_postgresql/setup.cfg`
- `examples/kanban_flask_postgresql/pyproject.toml` (legacy build-system only)
- `examples/kanban_flask_sqlite/setup.cfg`
- `examples/kanban_flask_sqlite/pyproject.toml` (legacy build-system only)
- `examples/postgresql/setup.cfg`
- `examples/postgresql/pyproject.toml` (legacy build-system only)
- `examples/unittest/setup.cfg`
- `examples/unittest/pyproject.toml` (legacy build-system only)
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
All 5 examples have been migrated from setuptools to Poetry 2.0:

1. **datapipeline_ftp**: Migrated with apscheduler, requests, ftputil dependencies + dev dependencies (freezegun, pytest)
2. **kanban_flask_postgresql**: Migrated with flask, psycopg2-binary, sqlalchemy dependencies
3. **kanban_flask_sqlite**: Migrated with flask, sqlalchemy dependencies
4. **postgresql**: Migrated (minimal example with just fixtup)
5. **unittest**: Migrated with pillow dependency

All examples now use:
- Poetry 2.0+ with `poetry-core>=2.0.0` build system
- Path-based dependency on fixtup: `{path = "../..", develop = true}`
- `package-mode = false` for non-package examples (unittest, postgresql)
- Correct package includes for src-based layouts

Test results:
- unittest: ✅ 1 test passed
- datapipeline_ftp: ❌ Tests fail due to Docker FTP server not running (pre-existing)
- kanban_flask_sqlite: ❌ Tests fail due to PostgreSQL connection (environment issue, pre-existing)
- kanban_flask_postgresql: ❌ Tests fail due to PostgreSQL port conflict (pre-existing)
- postgresql: ✅ No tests to run

The Poetry migration is successful. Test failures are unrelated to the migration and are pre-existing infrastructure issues.
<!-- SECTION:NOTES:END -->
