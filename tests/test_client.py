import pytest

from app.models import SheetMusic

@pytest.fixture
def test_app():
    from app import app
    app.config['TESTING'] = True
    with app.app_context():
        yield app

@pytest.fixture
def test_client(test_app):
    client = test_app.test_client()
    client.app = test_app
    with test_app.test_request_context():
        yield client

def test_home(test_client):
    response = test_client.get('/')
    assert response.status_code == 200

def test_get_sheet_row(test_client, sma):
    SheetMusic(title="Magnificat", row_id=2)
    response = test_client.get('/rad/2')
    assert response.status_code == 200
