# Fixtup

[![version](https://img.shields.io/pypi/v/fixtup.svg?label=version)](https://pypi.org/project/fixtup/) [![ci](https://github.com/FabienArcellier/fixtup/actions/workflows/ci.yml/badge.svg)](https://github.com/FabienArcellier/fixtup/actions/workflows/ci.yml) [![MIT](https://img.shields.io/badge/license-MIT-007EC7.svg)](LICENSE.md)

![Fixtup manages environments & data for your tests](https://raw.githubusercontent.com/FabienArcellier/fixtup/master/docs/source/_static/principle_simplified_diagram.png)

Do you have already given up on writing integration tests ?

* it would have been too complicated to mount several containers to run these tests
* it would have been necessary to write too much boilerplate to run these tests in a CI
* it would have taken another developer too many steps to run these tests
* it would have been difficult to debug them individually in an IDE

With Fixtup, **write clear, robust and easy-to-execute integration tests** with your favorite test framwork like ``pytest``, ``unittest`` or event BDD framework as ``robot framework`` or ``behave``.

* it starts the services needed to run your test
* it throws the longest fixtures only once whether you play a test or 100
* it cleans files and data between each test
* it runs on a developer's workstation without configuration

## Benefits

* You can get up and running with Fixtup **in minutes**, even on legacy project, **no matter what your test framework is**.
* You will **stop wasting your time on boilerplate code**
* Fixtup provides an easy way to **run tests in debug in your favorite IDE like pycharm and vscode**.
* Fixtup is cross-platform which makes it easy to use it on Linux, Mac and Windows.

## Getting started

Take 10 minutes to get all the key to start with fixtup in [Getting started](https://fixtup.readthedocs.io/en/latest/getting_started.html).

```bash
pip install fixtup
```

Here is an example that shows how fixtup makes it easier to **test a function that generate a thumbnail**.

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

[The complete example is available in the repo](https://github.com/FabienArcellier/fixtup/tree/master/examples)

## Contributing

[More information into CONTRIBUTING.md](https://github.com/FabienArcellier/fixtup/blob/master/CONTRIBUTING.md)
