from app import app
from models import *

db.create_all()
t_app = app.test_client()
name = 'some name'
email = 'test@mail.com'

def get_user():
    return User.query.filter_by(email=email).first()


def get_token():
    return dict(t_app.post('/login', json={'username': 'Nazar', 'password': '123'}).json)['access_token']


def get_ticket():
    return Ticket.query.filter_by(name=name).first()


def test_create_user_200():
    data = t_app.post('/user/create', json={'username': 'Nazar', 'email': email, 'password': '123'})
    assert '200' in str(data)


def test_create_ticket_200():
    data = t_app.post('/ticket', json={'name': name, 'description': 'description', 'price': '200',
                                       'endTimeReservation': '2013-01-12 15:27:43', 'reservationPrice': '100'},
                      headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '200' in str(data)


def test_create_ticket_204():
    data = t_app.post('/ticket',
                      json={'description': 'description', 'price': '200', 'endTimeReservation': '2013-01-12 15:27:43',
                            'reservationPrice': '100'}, headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '204' in str(data)


def test_ticket_findByStatus_200():
    data = t_app.get('/ticket/findByStatus', json={'status': 'available'},
                     headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '200' in str(data)


def test_ticket_findByStatus_404():
    data = t_app.get('/ticket/findByStatus', json={}, headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '404' in str(data)


def test_order_ticket_get_200():
    data = t_app.get('/ticket/' + str(get_ticket().id), headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '200' in str(data)


def test_order_ticket_get_404():
    data = t_app.get('/ticket/9999', headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '404' in str(data)


def test_order_ticket_put_200():
    data = t_app.put('/ticket/' + str(get_ticket().id),
                     json={'name': name, 'description': 'description', 'price': '300',
                           'endTimeReservation': '2013-01-12 15:27:43', 'reservationPrice': '100', 'status': 'end'},
                     headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '200' in str(data)


def test_order_ticket_delete_200():
    data = t_app.delete('/ticket/' + str(get_ticket().id), headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '200' in str(data)


def test_user_delete_201():
    data = t_app.delete('/user/' + str(get_user().id),
                        json={'username': 'Nazar', 'email': email, 'password': '123'},
                        headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '201' in str(data)
