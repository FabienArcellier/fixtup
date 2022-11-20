#!/usr/bin/env python
#
# This hook dumps the content of the ftp server before playing a test
import os
from typing import Optional

import ftputil
from ftputil import FTPHost


def ensure_ftp_is_empty(ftp: FTPHost, path: Optional[str]):
    list_doc = ftp.listdir(path)

    for name in list_doc:
        if name != "." and name != "..":
            if ftp.path.isfile(name):
                ftp.remove(name)
            else:
                ftp.rmtree(name)


with ftputil.FTPHost(host=os.getenv('FTP_HOST', 'localhost'), user=os.getenv('FTP_USER', None), passwd=os.getenv('FTP_PASS', None)) as ftp:
    ensure_ftp_is_empty(ftp, ftp.curdir)
