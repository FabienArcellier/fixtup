from sqlalchemy import Column, Integer, Text, ForeignKey
from kanban.database import Base


class BoardColumn(Base):
    __tablename__ = 'board_column'
    pid = Column(Integer, primary_key=True)
    step_name = Column(Text(), unique=True)
    wip_limit = Column(Integer)


class WorkItem(Base):
    __tablename__ = 'work_item'
    pid = Column(Integer, primary_key=True)
    column_pid = Column(Integer, ForeignKey('column.id'))
    title = Column(Text())
    description = Column(Integer)
