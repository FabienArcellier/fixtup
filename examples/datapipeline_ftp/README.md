# Datapipeline from API to FTP

This pipeline downloads data every minute from OpenWeather and archives it to an FTP server in csv format
every 10 minutes to an ftp server.

1. install the dependencies

```bash
pip3 install .[dev]
```

2. execute the tests

```bash
python3 -m unittest discover tests/integrations
```

Those examples show how you can use `fixtup hooks` to reset the content of the ftp between every tests. You should take a look at  :
* [tests/fixtures/ftp_server/.hooks/hook_setup_data.py](tests/fixtures/ftp_server/.hooks/hook_setup_data.py)


