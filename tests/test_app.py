from App import app

def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200

def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code in (200, 500)

def test_get_user():
    client = app.test_client()
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_noexistant_user():
    client = app.test_client()
    response = client.get("/users/999999")
    assert response.status_code == 404