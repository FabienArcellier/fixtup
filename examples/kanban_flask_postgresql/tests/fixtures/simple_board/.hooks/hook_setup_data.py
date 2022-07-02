#!/usr/bin/env python
#
# This hook is executed between each test and is intended
# to mount a dataset in a database or another system before playing the test.

import kanban.database
from kanban.database import db_session
from kanban.model import BoardColumn, WorkItem

kanban.database.reset_db()

db_session.add(BoardColumn(pid=1, step_name="TODO", wip_limit=None))
db_session.add(BoardColumn(pid=2, step_name="DOING", wip_limit=4))
db_session.add(BoardColumn(pid=3, step_name="DONE", wip_limit=None))
db_session.commit()

db_session.add(WorkItem(pid=1, title='implement feature AAA', column=1, description='xxxxxxxxxxxxxxxxxxxx'))
db_session.add(WorkItem(pid=2, title='implement feature BBB', column=1, description='xxxxxxxxxxxxxxxxxxxx'))
db_session.add(WorkItem(pid=3, title='implement feature CCC', column=3, description='xxxxxxxxxxxxxxxxxxxx'))
db_session.add(WorkItem(pid=12, title='implement feature XXX', column=1, description='xxxxxxxxxxxxxxxxxxxx'))
db_session.commit()
