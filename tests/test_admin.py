import os
import pytest

os.environ["SKY_ADMIN_SETTINGS"] = "../conf/admin.cfg"

import context
from skycrawler.admin import app


@pytest.fixture
def app_client():
    return app.test_client()


def test_index(app_client, data_test):
    page = app_client.get('/admin/')
    assert page.status_code == 200
