import os
os.environ["SKYCRAWLER_DB"] = ':memory:'

import pytest

import context
from skycrawler.database import db_session, init_db, drop_db
from skycrawler.model import Building, City


@pytest.fixture
def db_test():
    init_db()
    yield db_session
    drop_db()


@pytest.fixture
def data_test(db_test):

    montreal = City('Montreal', 100, 150)
    db_test.add(montreal)
    db_test.commit()

    building1 = Building('Building 1', 200, 50, 'http://fakelink', montreal, 'U/C', True)
    db_test.add(building1)
    building2 = Building('Building 2', 300, 80, 'http://fakelink2', montreal, 'U/C', True)
    db_test.add(building2)
    db_test.commit()
    return db_test
