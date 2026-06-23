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

# Test 1: Successful registration
def test_register_success(client):
    response = client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'securepass123'
    })
    assert response.status_code == 201
    assert b'registered successfully' in response.data

# Test 2: Successful login
def test_login_success(client):
    # First register
    client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'securepass123'
    })
    # Then login
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'securepass123'
    })
    assert response.status_code == 200
    assert b'access_token' in response.data

# Test 3: Access protected profile route with valid token
def test_profile_with_token(client):
    # Register and login
    client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'securepass123'
    })
    login_response = client.post('/login', json={
        'username': 'testuser',
        'password': 'securepass123'
    })
    token = login_response.get_json()['access_token']

    # Access profile
    response = client.get('/profile', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert b'testuser' in response.data