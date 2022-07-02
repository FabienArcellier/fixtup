import os
import tempfile

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine(os.getenv('SQLITE_DSN', f'sqlite:///{tempfile.gettempdir()}/kanban.db'))
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base.query = db_session.query_property()


def reset_db():
    """
    reset all database tables.

    SQLAlchemy destroys tables and then recreates them. This is the guarantee of also
    reinitializing sequences and of avoiding the integrity errors which result therefrom.
    """

    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling reset_db()
    import kanban.model
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
