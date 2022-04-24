import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = None
_db_session = None
Base = declarative_base()


def db_connect():
    global engine, _db_session
    if not engine:
        engine = create_engine(os.getenv('SQLITE_DSN', 'sqlite:///kanban.db'))

    if not _db_session:
        _db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        Base.query = _db_session.query_property()


def db_dispose():
    """
    dispose all resources relative to the database. This method
    should be use if you want to mount a connection to a brand
    new database. It happens mainly in the tests
    """
    global engine, _db_session
    if _db_session:
        _db_session.close()
        Base.query = None
        _db_session = None

    if engine:
        engine.dispose()
        engine = None


def db_session():
    db_connect()
    return _db_session


def db_init():
    db_connect()
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import kanban.model
    Base.metadata.create_all(bind=engine)
