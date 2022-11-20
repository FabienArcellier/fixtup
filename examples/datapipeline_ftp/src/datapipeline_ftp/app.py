import csv
import dataclasses
import logging
import os
import tempfile
from datetime import datetime, timedelta
from typing import List, Tuple, Optional

import ftputil
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('datapipeline_ftp')


@dataclasses.dataclass
class OpenWeatherDataset:
    records: List[Tuple[datetime, Optional[dict]]] = dataclasses.field(default_factory=list)

    def enqueue(self, time: datetime, record: dict):
        self.records.append((time, record))

    def pop(self) -> List[Tuple[datetime, dict]]:
        records = self.records
        self.records = []

        return records


def main():
    dataset = OpenWeatherDataset()
    scheduler = BlockingScheduler()
    scheduler.add_job(pipeline_weather_acquisition, kwargs={'dataset': dataset}, trigger='interval', minutes=1)
    scheduler.add_job(pipeline_weather_publication, kwargs={'dataset': dataset}, trigger='interval', minutes=10)
    scheduler.start()


def pipeline_weather_acquisition(dataset: OpenWeatherDataset):
    openweather__api_key = os.getenv('OPENWEATHER__API_KEY', None)
    if openweather__api_key is None:
        print("You have to set a valid open weather api key.")
        print("$ OPENWEATHER__API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxx")
        return

    now = datetime.utcnow()
    url = f'https://api.openweathermap.org/data/2.5/weather?lat=45.76&lon=4.83&APPID={openweather__api_key}'
    frame = now - timedelta(seconds=now.second, microseconds=now.microsecond)
    try:
        r = requests.get(url)
        weather_info = r.json()
        logger.info(f'{now} - {url} - OK')
        dataset.enqueue(frame, weather_info)
    except:
        logger.warning(f'{now} - {url} - KO')
        dataset.enqueue(frame, None)


def pipeline_weather_publication(dataset: OpenWeatherDataset):
    records = dataset.pop()

    ftp_host = os.getenv('FTP_HOST', 'localhost')
    ftp_user = os.getenv('FTP_USER', None)
    ftp_pwd = os.getenv('FTP_PASS', None)

    fieldnames = ['timestamp', 'measure_timestamp', 'ok', 'wind_speed', 'humidity']
    content = []
    for timestamp, record in records:
        row = {}
        row['timestamp'] = timestamp.isoformat()
        if record is not None:
            row['ok'] = 1
            wind_section = record.get('wind', {})
            row['wind_speed'] = wind_section.get('speed', None)
            row['measure_timestamp'] = record.get('dt', 0)
            main_section = record.get('main', {})
            row['humidity'] = main_section.get("humidity")
        else:
            row['ok'] = 0

        content.append(row)

    now = datetime.utcnow()
    file_timestamp = now - timedelta(minutes=now.minute % 10, microseconds=now.microsecond)
    filename = f"file-{file_timestamp.strftime('%Y-%m-%dT%H-%M')}.csv"

    with tempfile.TemporaryFile('a+') as filep:
        csv_file = csv.DictWriter(filep, fieldnames)
        csv_file.writeheader()
        for row in content:
            csv_file.writerow(row)

        filep.seek(0)

        with ftputil.FTPHost(host=ftp_host, user=ftp_user, passwd=ftp_pwd) as host:
            with host.open(filename, 'w') as ftp_filep:
                ftp_filep.write(filep.read())


if __name__ == "__main__":
    main()
