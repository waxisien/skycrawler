import os
import pytest

os.environ["MY_GOOGLE_MAP_KEY"] = 'test'

from skycrawler.app import app


@pytest.fixture
def app_client():
    return app.test_client()


def test_index(app_client, data_test):
    page = app_client.get('/')
    assert page.status_code == 200


def test_raw(app_client, data_test):
    page = app_client.get('/raw')
    assert page.status_code == 200
