from app import app
from models import *
from tests.config import *

db.create_all()
t_app = app.test_client()


def get_user():
    return User.query.filter_by(email=email).first()


def get_token():
    return dict(t_app.post('/login', json={'username': 'Nazar', 'password': '123'}).json)['access_token']


def test_create_user_200():
    data = t_app.post('/user/create', json={'username': 'Nazar', 'email': email, 'password': '123'})
    assert '200' in str(data)


def test_create_user_204():
    data = t_app.post('/user/create', json={'username': 'Nazar', 'email': email})
    assert '204' in str(data)


def test_create_user_404():
    data = t_app.post('/user/create', json={'username': 'Nazar', 'email': email, 'password': '123'})
    assert '400' in str(data)


def test_user_404():
    data = t_app.put('/user/99999', json={'username': 'New name Nazar', 'email': email, 'password': '123'},
                     headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '404' in str(data)


def test_user_put_201():
    data = t_app.put('/user/' + str(get_user().id),
                     json={'username': 'Nazar', 'email': email, 'password': '123'},
                     headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '201' in str(data)


def test_login_401():
    data = t_app.post('/login', json={'username': 'Nazar', 'password': '1234'})
    assert '401' in str(data)


def test_login_404():
    data = t_app.post('/login')
    assert '404' in str(data)


def test_login_200():
    data = t_app.post('/login', json={'username': 'Nazar', 'password': '123'})
    assert '200' in str(data)


def test_user_delete_201():
    data = t_app.delete('/user/' + str(get_user().id),
                        json={'username': 'Nazar', 'email': email, 'password': '123'},
                        headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '201' in str(data)
