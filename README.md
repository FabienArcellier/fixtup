# Fixtup

You will love writing integration tests in python with ``Fixtup``.

![outline schematic from fixtup](docs/source/_static/principle_simplified_diagram.png)

Some of your tests need a database, a folder with data, dedicated environment variables, ``Fixtup`` provides all of this for you. Don't even bother to take care of the cleaning, it releases by itself the resources that it has provisioned.

``Fixtup`` makes it easy to use external dependencies in your tests. It integrates
to your favorite test framework like pytest, unitest or even BDD framework like robot framework or behave.

## Getting started

Take 10 minutes to get all the key to start with fixtup in [Getting started]().

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

La documentation offre plus d'exemples :

* mutualiser les fixtures dans le setup et teardown
* utiliser fixtup avec le plugin pytest
* instancier une base de donnée redis avec fixtup
* spécifier des variables d'environnement à utiliser avec fixtup
* ...

## Contributing

[More information into CONTRIBUTING.md](./CONTRIBUTING.md)
