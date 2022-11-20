import os
import unittest
from datetime import datetime

from freezegun import freeze_time
import fixtup
import ftputil

from datapipeline_ftp.app import pipeline_weather_publication, OpenWeatherDataset


@freeze_time('2022-11-20T12:10')
def test_pipeline_weather_publication_should_export_a_dataset_on_a_ftp():
    with fixtup.up('ftp_server'):
        # Assign
        dataset = OpenWeatherDataset()
        dataset.enqueue(datetime(2022, 11, 20, 12, 5), {'wind': {'speed': 15}, 'main': {'humidity': 3}})
        dataset.enqueue(datetime(2022, 11, 20, 12, 6), {'wind': {'speed': 15}, 'main': {'humidity': 3}})
        dataset.enqueue(datetime(2022, 11, 20, 12, 7), {'wind': {'speed': 15}, 'main': {'humidity': 3}})
        dataset.enqueue(datetime(2022, 11, 20, 12, 8), {'wind': {'speed': 15}, 'main': {'humidity': 3}})
        dataset.enqueue(datetime(2022, 11, 20, 12, 9), {'wind': {'speed': 15}, 'main': {'humidity': 3}})
        dataset.enqueue(datetime(2022, 11, 20, 12, 10), {'wind': {'speed': 15}, 'main': {'humidity': 3}})

        # Acts
        pipeline_weather_publication(dataset)

        # Assert
        with ftputil.FTPHost(host=os.getenv('FTP_HOST', 'localhost'), user=os.getenv('FTP_USER', None), passwd=os.getenv('FTP_PASS', None)) as host:
            names = host.listdir(host.curdir)
            assert len(names) == 1
            assert 'file-2022-11-20T12-10.csv' in names

@freeze_time('2022-11-20T12:23')
def test_pipeline_weather_publication_should_round_the_filename_to_the_ten_minutes():
    with fixtup.up('ftp_server'):
        # Assign
        dataset = OpenWeatherDataset()
        dataset.enqueue(datetime(2022, 11, 20, 12, 5), {'wind': {'speed': 15}, 'main': {'humidity': 3}})
        dataset.enqueue(datetime(2022, 11, 20, 12, 6), {'wind': {'speed': 15}, 'main': {'humidity': 3}})
        dataset.enqueue(datetime(2022, 11, 20, 12, 7), {'wind': {'speed': 15}, 'main': {'humidity': 3}})
        dataset.enqueue(datetime(2022, 11, 20, 12, 8), {'wind': {'speed': 15}, 'main': {'humidity': 3}})
        dataset.enqueue(datetime(2022, 11, 20, 12, 9), {'wind': {'speed': 15}, 'main': {'humidity': 3}})
        dataset.enqueue(datetime(2022, 11, 20, 12, 10), {'wind': {'speed': 15}, 'main': {'humidity': 3}})

        # Acts
        pipeline_weather_publication(dataset)

        # Assert
        with ftputil.FTPHost(host=os.getenv('FTP_HOST', 'localhost'), user=os.getenv('FTP_USER', None), passwd=os.getenv('FTP_PASS', None)) as host:
            names = host.listdir(host.curdir)
            assert len(names) == 1
            assert 'file-2022-11-20T12-20.csv' in names

if __name__ == '__main__':
    unittest.main()
