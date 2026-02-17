# Fixtup

Test your python application beyond your code !

[![version](https://img.shields.io/pypi/v/fixtup.svg?label=version)](https://pypi.org/project/fixtup/) [![ci](https://github.com/FabienArcellier/fixtup/actions/workflows/ci.yml/badge.svg)](https://github.com/FabienArcellier/fixtup/actions/workflows/ci.yml) [![MIT](https://img.shields.io/badge/license-MIT-007EC7.svg)](LICENSE.md)

![Fixtup manages disposable environments & data for your tests](https://raw.githubusercontent.com/FabienArcellier/fixtup/master/docs/source/_static/principle_simplified_diagram.png)

**write clear, robust and easy-to-execute system integration tests** with your favorite test framwork like ``pytest``, ``unittest`` or event BDD framework as ``robot framework`` or ``behave``.

* it starts the services needed to run your test
* it mount the longest fixtures only once whether you play a test or 100
* it cleans files and data between each test
* it runs on a developer's workstation without configuration
* it can be debugged step by step in your favorite IDE

## Benefits

* You can get up and running with Fixtup **in minutes**, even on legacy project, **no matter what your test framework is**.
* You will **stop wasting your time on boilerplate code**
* Fixtup provides an easy way to **run tests in debug in your favorite IDE like pycharm and vscode**.
* Fixtup is cross-platform which makes it easy to use it on Linux, Mac and Windows.

## Getting started

**write clear, robust and easy-to-execute system integration tests** in 5 minutes.

```bash
$ poetry init
$ poety add --dev fixtup
```

```bash
$ poetry run fixtup init
$ poetry run fixtup new
Choose a fixture identifier : thumbnail_context
Mount environment variables on this fixture (y/n) [n]
Mount docker container on this fixture (y/n) [n]
```

We will use this fixture to mount a directory with existing picture `file.png` and test
our `thumbnail` function is working well.

```python
def test_thumbnail_should_generate_thumbnail(self):

    # Magic happens with the instruction fixtup.up
    with fixtup.up('thumbnail_context') as f:
        # Given
        wd = os.getcwd()
        original_file = os.directory.join(wd, 'file.png')
        expected_thumbnail_file = os.directory.join(wd, 'file_t.png')

        # Then
        thumbnail(original_file, expected_thumbnail_file)

        # Then
        self.assertTrue(os.directory.isfile(expected_thumbnail_file)
```

Fixtup mount the fixture `thumbnail_context` in temporary directory. At the end of the test, it clean up everything for you
Want more ? [Fixtup even mount your containers, take a try](https://fixtup.readthedocs.io/en/latest/handbook.html#mount-a-postgresql-database-in-a-test).

[The complete example is available in the repo](https://github.com/FabienArcellier/fixtup/tree/master/examples)

## Installation

### Using pip

```bash
pip install fixtup
```

### Using Poetry (recommended for development)

```bash
poetry add --group dev fixtup
```

## Development Setup

This project uses [Poetry](https://python-poetry.org/) for dependency management and packaging.

### Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/docs/#installation)

### Setup

```bash
# Clone the repository
git clone https://github.com/FabienArcellier/fixtup.git
cd fixtup

# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

### Running Tests

```bash
# Run all tests
poetry run alfred tests

# Run specific test suites
poetry run alfred tests:units
poetry run alfred tests:integrations
poetry run alfred tests:acceptances
```

### Linting

```bash
poetry run alfred lint
```

### Building Documentation

```bash
poetry run alfred docs:build
poetry run alfred docs:display
```

## Contributing

[More information into CONTRIBUTING.md](https://github.com/FabienArcellier/fixtup/blob/master/CONTRIBUTING.md)
