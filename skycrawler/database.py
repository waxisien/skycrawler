import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 'check_same_thread=false': as long as only one thread writes in db (searchengine script) we are safe.
sqlite_url = 'sqlite:///' + os.environ['SKYCRAWLER_DB'] + '?check_same_thread=false'
engine = create_engine(sqlite_url, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import skycrawler.model
    Base.metadata.create_all(bind=engine)


def drop_db():
    import skycrawler.model
    Base.metadata.drop_all(bind=engine)
