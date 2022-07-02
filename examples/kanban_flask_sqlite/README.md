# Sandbox : kanban API with flask and sqlite

This minimal example show with unittest how fixtup help you to test a flask application that work with sqlite. An sqlite database is mounted in the `tmp/kanban.db` folder

1. install the dependencies

```bash
pip3 install .[dev]
```

2. execute the tests

```bash
python3 -m unittest discover tests/acceptances
```

Those examples show how you can use `fixtup hooks` to load required dataset for your tests. You should take a look at :
* [tests/fixtures/simple_board/.hooks/hook_setup_data.py](tests/fixtures/simple_board/.hooks/hook_setup_data.py)
* [tests/fixtures/simple_board_with_wip/.hooks/hook_setup_data.py](tests/fixtures/simple_board_with_wip/.hooks/hook_setup_data.py)


