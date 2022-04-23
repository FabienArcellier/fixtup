#!/usr/bin/env python
#
# rename this file into hook_started.py to activate
# this hook.
#
# this hook is executed after the environment has been started
#
# It's a way to check if the environment is ready for the test.
#  * check if a port is listening before executing the test
#  * check if a database in postgresql is up and mounted
#

import kanban.database

kanban.database.init_db()
