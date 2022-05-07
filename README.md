# Fixtup

[![version](https://img.shields.io/pypi/v/fixtup.svg?label=version)](https://pypi.org/project/fixtup/) [![ci](https://github.com/FabienArcellier/fixtup/actions/workflows/ci.yml/badge.svg)](https://github.com/FabienArcellier/fixtup/actions/workflows/ci.yml) [![MIT](https://img.shields.io/badge/license-MIT-007EC7.svg)](LICENSE.md)

You will love writing integration tests in python with ``Fixtup``.

![outline schematic from fixtup](https://raw.githubusercontent.com/FabienArcellier/fixtup/master/docs/source/_static/principle_simplified_diagram.png)

Some of your tests need a database, a folder with data, dedicated environment variables, ``Fixtup`` provides all of this for you. Don't even bother to take care of the cleaning, it releases by itself the resources that it has provisioned.

``Fixtup`` makes it easy to use external dependencies in your tests. It integrates
to your favorite test framework like pytest, unitest or even BDD framework like robot framework or behave.

## Benefits

* You can get up and running with Fixtup **in minutes**, even on legacy project, **no matter what your test framework is**.
* You will **stop wasting your time on boilerplate code** to create a database, that's all done in one line with Fixtup.
* Fixtup provides an easy way to **run tests in debug in your favorite IDE, pycharm and vscode**.
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
