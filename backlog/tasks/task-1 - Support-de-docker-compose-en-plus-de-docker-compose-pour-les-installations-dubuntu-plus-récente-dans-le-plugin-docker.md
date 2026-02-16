---
id: TASK-1
title: >-
  Support de docker compose en plus de docker-compose pour les installations
  d'ubuntu plus récente dans le plugin docker
status: Review
assignee: []
created_date: '2026-02-16 22:58'
updated_date: '2026-02-16 23:04'
labels:
  - docker
  - ubuntu
  - compatibility
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Modern Docker installations on Ubuntu 22.04+ and other recent distributions use the `docker compose` command (Docker Compose V2 plugin) instead of the legacy standalone `docker-compose` binary. The current docker plugin only supports the legacy `docker-compose` command, causing failures on systems with modern Docker installations.

This task involves implementing automatic detection and support for both command variants to ensure compatibility across different Docker installation methods.

### Impacts

#### Positive
- Compatibility with modern Docker installations on Ubuntu 22.04+, Debian 12+, and other recent distributions
- Support for Docker Desktop and Docker Engine with Compose V2 plugin
- Future-proofing as Docker Compose V1 is deprecated
- No breaking changes for existing users with legacy installations

#### Negative
- Slightly increased complexity in command detection logic
- Need to test both command variants in CI

#### Further consideration
- Consider adding a configuration option to force a specific command variant
- Document the detection behavior for users
- Monitor Docker's deprecation timeline for Compose V1
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Implement automatic detection of available docker compose command (`docker compose` vs `docker-compose`)
- [x] #2 Modify `get_docker_compose_cmd()` to return the appropriate command based on availability
- [x] #3 Add helper function to detect which command is available on the system
- [x] #4 Update all docker compose invocations to use the detected command
- [x] #5 Unit tests cover the detection logic for both scenarios
- [x] #6 Integration tests pass with both command variants
- [ ] #7 Documentation updated to explain the automatic detection behavior
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
### Steps

1. **Analyze current implementation**
   - Review `get_docker_compose_cmd()` in `src/fixtup/plugins/docker.py`
   - Identify all locations where docker-compose is invoked

2. **Implement command detection**
   - Create `_detect_docker_compose_cmd()` helper function
   - Check availability of `docker compose` (V2 plugin) first
   - Fall back to `docker-compose` (V1 standalone) if needed
   - Cache the detected command to avoid repeated checks

3. **Update command execution**
   - Modify `get_docker_compose_cmd()` to use detected command
   - Handle the different invocation syntax:
     - V2: `docker['compose']` (subcommand)
     - V1: `docker-compose` (standalone)

4. **Add unit tests**
   - Test detection logic when only V1 is available
   - Test detection logic when only V2 is available
   - Test detection logic when both are available (prefer V2)

5. **Update integration tests**
   - Ensure existing tests work with both variants
   - Add test coverage for the detection mechanism

6. **Documentation**
   - Update plugin documentation with compatibility notes

### Files

- `src/fixtup/plugins/docker.py` - Main plugin implementation
- `tests/integrations/plugins/test_docker.py` - Integration tests
- `tests/units/plugins/` - Unit tests (create if needed)
<!-- SECTION:PLAN:END -->
