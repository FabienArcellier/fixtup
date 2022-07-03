from dataclasses import dataclass

from sqlalchemy import Column, Integer, Text, ForeignKey
from kanban.database import Base


@dataclass
class BoardColumn(Base):
    __tablename__ = 'board_column'
    pid: int
    step_name: str
    wip_limit: int

    pid = Column(Integer, primary_key=True)
    step_name = Column(Text, unique=True)
    wip_limit = Column(Integer, nullable=True)


@dataclass
class WorkItem(Base):
    __tablename__ = 'work_item'
    pid: int
    column: int
    title: str
    description: str

    pid = Column(Integer, primary_key=True)
    column = Column(Integer, ForeignKey('board_column.pid'))
    title = Column(Text)
    description = Column(Text)
