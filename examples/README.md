These examples show how to use Fixtup. Each example illustrates how to implement a specific feature in a real-world scenario.

## Requirements

All examples use [Poetry](https://python-poetry.org/) for dependency management. Make sure you have Poetry 2.0+ installed:

```bash
pip install poetry>=2.0.0
```

## Running the Examples

Each example is a standalone Poetry project with fixtup configured as a local dependency. This allows you to test changes to fixtup immediately without publishing to PyPI.

```bash
# Navigate to an example directory
cd examples/unittest

# Install dependencies
poetry install

# Run the tests
poetry run pytest
```

## Examples

* [unittest](unittest): Shows how fixtup helps you test a function that generates a thumbnail from an image using unittest
* [kanban_flask_sqlite](kanban_flask_sqlite): Shows how to write integration and acceptance tests on a Flask application that works with SQLite
* [kanban_flask_postgresql](kanban_flask_postgresql): Shows how to test a Flask application with PostgreSQL using Docker containers
* [datapipeline_ftp](datapipeline_ftp): Shows how fixtup helps test a data pipeline that uploads to an FTP server
* [postgresql](postgresql): Shows how to use fixtup with PostgreSQL databases

## Troubleshooting

### Poetry install fails

If `poetry install` fails, ensure:
1. You're in the example directory (e.g., `examples/unittest/`)
2. The main fixtup project is at the expected relative path (`../..`)
3. You have Poetry 2.0+ installed: `poetry --version`

### Import errors

If you see import errors when running tests, make sure you've run `poetry install` in the example directory. The fixtup package is installed as an editable dependency from the local path.

### Lock file issues

If you encounter lock file conflicts, regenerate it:

```bash
poetry lock --no-update
poetry install
```
