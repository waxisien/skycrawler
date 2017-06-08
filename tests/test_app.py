import os
import pytest

os.environ["SKYCRAWLER_DB"] = ':memory:'
os.environ["MY_GOOGLE_MAP_KEY"] = 'test'

import context
from skycrawler.app import app
from skycrawler.database import db_session, init_db, drop_db
from skycrawler.model import Building, City


@pytest.fixture
def app_client():
    return app.test_client()


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


def test_index(app_client, data_test):
    page = app_client.get('/')
    assert page.status_code == 200


def test_raw(app_client, data_test):
    page = app_client.get('/raw')
    assert page.status_code == 200
