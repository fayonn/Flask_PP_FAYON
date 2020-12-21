from migrate import app, db
from models import *

db.create_all()
t_app = app.test_client()
email = 'test@mail.com'


def get_user():
    return User.query.filter_by(email=email).first()


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
    data = t_app.put('/user/99999', json={'username': 'New name Nazar', 'email': email, 'password': '123'})
    assert '404' in str(data)


def test_user_put_201():
    data = t_app.put('/user/' + str(get_user().id),
                     json={'username': 'New name Nazar', 'email': email, 'password': '123'})
    assert '201' in str(data)


def test_user__put_400():
    data = t_app.put('/user/' + str(get_user().id), json={'email': email, 'password': '123'})
    assert '400' in str(data)


def test_user_delete_201():
    data = t_app.delete('/user/' + str(get_user().id),
                        json={'username': 'New name Nazar', 'email': email, 'password': '123'})
    assert '201' in str(data)
