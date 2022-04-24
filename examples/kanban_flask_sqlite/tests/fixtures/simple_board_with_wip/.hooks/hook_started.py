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
from kanban.model import BoardColumn, WorkItem

kanban.database.db_init()
dbsession = kanban.database.db_session()

dbsession.add(BoardColumn(pid=1, step_name="TODO", wip_limit=None))
dbsession.add(BoardColumn(pid=2, step_name="DOING", wip_limit=4))
dbsession.add(BoardColumn(pid=3, step_name="REVIEW", wip_limit=1))
dbsession.add(BoardColumn(pid=4, step_name="DONE", wip_limit=None))

dbsession.commit()

dbsession.add(WorkItem(pid=1, title='implement feature AAA', column=1, description='xxxxxxxxxxxxxxxxxxxx'))
dbsession.add(WorkItem(pid=2, title='implement feature BBB', column=1, description='xxxxxxxxxxxxxxxxxxxx'))
dbsession.add(WorkItem(pid=3, title='implement feature CCC', column=4, description='xxxxxxxxxxxxxxxxxxxx'))
dbsession.add(WorkItem(pid=11, title='implement feature WWW', column=3, description='xxxxxxxxxxxxxxxxxxxx'))
dbsession.add(WorkItem(pid=12, title='implement feature XXX', column=1, description='xxxxxxxxxxxxxxxxxxxx'))
dbsession.commit()
