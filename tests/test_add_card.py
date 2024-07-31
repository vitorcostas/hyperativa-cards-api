import pytest
from flask_jwt_extended import create_access_token
from app import start
from app import db
from app.models import User


@pytest.fixture(scope='module')
def test_client():
    app = start()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()


@pytest.fixture(scope='module')
def new_user():
    user = User(username='testuser', password='testpassword')
    return user


@pytest.fixture(scope='module')
def token(new_user, test_client):
    db.session.add(new_user)
    db.session.commit()
    access_token = create_access_token(identity={'id': new_user.id, 'username': new_user.username})
    return access_token


def test_add_card_file_user_not_found(test_client):
    token = create_access_token(identity={'id': 9999, 'username': 'nonexistent'})

    data = {'card_number': 12313131313131}
    headers = {
        'Authorization': f'Bearer {token}',
        'content-type': 'application/json'
    }
    response = test_client.post(
        'http://localhost:8080/api/card/add_card',
        json=data,
        headers=headers
    )
    assert response.status_code == 404
    assert response.json['message'] == 'User not found'


def test_add_card_file_missing_authorization(test_client):
    data = {'card_number': 12313131313131}
    response = test_client.post(
        'http://localhost:8080/api/card/add_card',
        json=data
        , headers={'content-type': 'application/json'}
    )
    assert response.status_code == 403
    assert response.json['message'] == 'Missing Authorization Header'


def test_add_card_file_no_file(test_client, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'content-type': 'application/json'
    }
    response = test_client.post(
        'http://localhost:8080/api/card/add_card',
        json={},
        headers=headers
    )
    assert response.status_code == 400
    json = response.json
    assert json['errors'] == {'card_number': "'card_number' is a required property"}
