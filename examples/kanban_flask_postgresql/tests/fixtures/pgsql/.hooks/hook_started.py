from time import sleep

import fixtup

fixtup.helper.wait_port(5432, timeout=2000)
sleep(2)
