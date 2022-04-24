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

kanban.database.init_db()
dbsession = kanban.database.db_session()

todo_column = BoardColumn(pid=1, step_name="TODO", wip_limit=None)
doing_column = BoardColumn(pid=2, step_name="DOING", wip_limit=4)
done_column = BoardColumn(pid=3, step_name="DONE", wip_limit=None)

dbsession.add(todo_column)
dbsession.add(doing_column)
dbsession.add(done_column)
dbsession.commit()

dbsession.add(WorkItem(pid=1, title='implement feature AAA', column=1, description='xxxxxxxxxxxxxxxxxxxx'))
dbsession.add(WorkItem(pid=2, title='implement feature BBB', column=1, description='xxxxxxxxxxxxxxxxxxxx'))
dbsession.add(WorkItem(pid=3, title='implement feature CCC', column=3, description='xxxxxxxxxxxxxxxxxxxx'))
dbsession.add(WorkItem(pid=12, title='implement feature XXX', column=1, description='xxxxxxxxxxxxxxxxxxxx'))
dbsession.commit()
