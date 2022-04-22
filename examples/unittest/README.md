# Sandbox : fixtup with unittests

This minimal example show with unittest how fixtup help you to test a function that generate thumbnail from images.

1. install the dependencies

```bash
pip3 install .[dev]
```

2. execute integration tests

```bash
python3 -m unittest discover tests/integrations
```

The test `test_thumbnail_should_generate_thumbnail` will copy the directory `./tests/fixtures/thumbnail_context`, resize the image `file.png` and check the result is present. At the end of the test, the directory is cleanup.
