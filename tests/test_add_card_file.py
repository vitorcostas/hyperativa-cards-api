import pytest
from io import BytesIO
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

    data = (
        b"C1     4456897922969999\n"
        b"C2     4456897999999999\n"
    )
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = test_client.post(
        'http://localhost:8080/api/card/add_card_file',
        data={'file': (BytesIO(data), 'test.txt')},
        headers=headers
    )
    assert response.status_code == 404
    assert response.json['message'] == 'User not found'


def test_add_card_file_missing_authorization(test_client):
    data = (
        b"C1     4456897922969999\n"
        b"C2     4456897999999999\n"
    )
    response = test_client.post(
        'http://localhost:8080/api/card/add_card_file',
        data={'file': (BytesIO(data), 'test.txt')}
        , headers={'content-type': 'application/json'}
    )
    assert response.status_code == 403
    assert response.json['message'] == 'Missing Authorization Header'


def test_add_card_file_no_file(test_client, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = test_client.post(
        'http://localhost:8080/api/card/add_card_file',
        data={},
        headers=headers
    )
    assert response.status_code == 400
    assert response.json['message'] == {'file': 'Missing required parameter in an uploaded file'}
