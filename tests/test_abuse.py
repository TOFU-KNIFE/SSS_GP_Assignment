import pytest
from app import create_app, db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

# Abuse Test 1: Login with wrong password
def test_login_wrong_password(client):
    client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'securepass123'
    })
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert b'Invalid credentials' in response.data

# Abuse Test 2: SQL injection attempt in login
def test_sql_injection_login(client):
    response = client.post('/login', json={
        'username': "admin' OR '1'='1",
        'password': "' OR '1'='1"
    })
    assert response.status_code == 401

# Abuse Test 3: Access profile without token
def test_profile_without_token(client):
    response = client.get('/profile')
    assert response.status_code == 401

# Abuse Test 4: Register with missing fields
def test_register_missing_fields(client):
    response = client.post('/register', json={
        'username': 'testuser'
    })
    assert response.status_code == 400
    assert b'required' in response.data

# Abuse Test 5: Register with weak password
def test_register_weak_password(client):
    response = client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': '123'
    })
    assert response.status_code == 400
    assert b'8 characters' in response.data