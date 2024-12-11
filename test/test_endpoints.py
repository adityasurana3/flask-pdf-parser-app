import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_upload_endpoint(client):
    data = {'file': (open('/home/aditya/Documents/Flask/sample.pdf', 'rb'), 'sample.pdf')}
    response = client.post('/upload', data=data)
    assert response.status_code == 200
    assert 'unique_id' in response.json

def test_status_endpoint(client):
    response = client.get('/status/fake_id')
    assert response.status_code == 404
