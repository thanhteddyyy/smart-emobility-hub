import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import createApp          # noqa: E402
from data import mock_data as db   # noqa: E402


@pytest.fixture(autouse=True)
def freshData():
    """Mỗi test bắt đầu với dữ liệu gốc."""
    db.resetData()


@pytest.fixture
def client():
    app = createApp(startSimulator=False)
    app.config["TESTING"] = True
    return app.test_client()


@pytest.fixture
def loginAs(client):
    def _login(email, password="123456"):
        return client.post("/login", data={"email": email, "password": password})
    return _login
