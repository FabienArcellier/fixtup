# AGENTS.md - Guidelines for AI Coding Agents

This file contains guidelines for AI coding agents working on the fixtup repository.

## Project Overview

Fixtup is a Python library for managing disposable test environments and fixtures. It supports pytest, unittest, and BDD frameworks.

## Build/Lint/Test Commands

All commands use `alfred-cli` as the build engine:

```bash
# Full CI pipeline
alfred ci

# Run linting (type checking with mypy)
alfred lint

# Run all tests
alfred tests

# Run specific test suites
alfred tests:units          # Unit tests
alfred tests:integrations   # Integration tests
alfred tests:acceptances    # Acceptance tests

# Run a single test file (using unittest directly)
python -m unittest tests.units.entity.test_fixture
python -m unittest tests.acceptances.test_fixtup

# Run a single test method
python -m unittest tests.units.entity.test_fixture.TestFixture.test_create_from_template_should_extract_fixture_identifier_from_the_path

# Documentation
alfred docs:build    # Build docs
alfred docs:display  # Display docs
alfred docs:check    # Check docs

# Distribution
alfred dist:build    # Build distribution
alfred publish       # Publish to PyPI
```

## Development Environment Setup

```bash
# Install dependencies (uses pipenv)
pipenv install --dev
pipenv shell
```

## Code Style Guidelines

### Imports

* Group imports: stdlib, third-party, local
* Use absolute imports for project code
* Example:
  ```python
  import os
  from typing import Generator, Optional
  
  import attr
  
  from fixtup.entity.fixture_template import FixtureTemplate
  ```

### Type Hints

* Use type hints for function signatures
* Use `typing` module for complex types (Generator, Optional, etc.)
* Run `alfred lint` to validate type consistency

### Naming Conventions

* Classes: PascalCase (e.g., `FixtureTemplate`, `FixtupException`)
* Functions/methods: snake_case (e.g., `test_up_should_mount_fixture`)
* Constants: UPPER_CASE (e.g., `ROOT_DIR`)
* Private methods: prefix with underscore (e.g., `_setup_fixture`)

### Testing

* Use `unittest` framework
* Test files: `test_<module>.py`
* Test classes: `Test<ClassName>` or descriptive name
* Test methods: descriptive snake_case starting with `test_`
* Structure: Arrange, Act, Assert comments
* Use `.fake()` factory methods for test entities

### Error Handling

* Custom exceptions inherit from `FixtupException`
* Located in `src/fixtup/exceptions.py`
* Include descriptive error messages

### Project Structure

* Source code: `src/fixtup/`
* Tests: `tests/units/`, `tests/integrations/`, `tests/acceptances/`
* Build commands: `alfred/`
* Fixtures for tests: `tests/fixtures/`

### Entity Classes

* Use `attrs` library with `@attr.s` decorator
* Provide `.fake()` class method for testing
* Example:
  ```python
  @attr.s
  class Fixture:
      identifier: str = attr.ib()
      directory: str = attr.ib()
      
      @classmethod
      def fake(cls, **kwargs) -> 'Fixture':
          return Fixture(...)
  ```

### Configuration

* Dependencies in `setup.cfg`
* mypy config in `setup.cfg`
* Version in `src/fixtup/__init__.py`

## CI/CD

GitHub Actions runs `alfred ci --no-docs` on Python 3.8-3.11.

## Task Management with Backlog.md

This project uses Backlog.md for task management. Use the following MCP tools:

```bash
# List tasks
backlog_md_task_list

# Search tasks
backlog_md_task_search "query"

# View a task
backlog_md_task_view TASK-123

# Create a new task
backlog_md_task_create --title "Task title" --description "Description"

# Edit a task
backlog_md_task_edit TASK-123 --status "In Progress"

# Complete a task
backlog_md_task_complete TASK-123

# Archive a task
backlog_md_task_archive TASK-123

# List milestones
backlog_md_milestone_list

# Create/Edit/Archive documents
backlog_md_document_list
backlog_md_document_view DOC-123
backlog_md_document_create --title "Doc title" --content "Content"
```

Workflow guides available:
- `backlog_md_get_workflow_overview` - General workflow
- `backlog_md_get_task_creation_guide` - Creating tasks
- `backlog_md_get_task_execution_guide` - Executing tasks
- `backlog_md_get_task_finalization_guide` - Finalizing tasks
