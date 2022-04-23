import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from kanban.app import app

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


def db_session():
    db_connect()
    return _db_session


def init_db():
    db_connect()
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import kanban.model
    Base.metadata.create_all(bind=engine)


@app.teardown_appcontext
def shutdown_session(exception=None):
    if _db_session is not None:
        _db_session.remove()
