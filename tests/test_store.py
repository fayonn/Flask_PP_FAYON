from app import app
from models import *
from tests.config import *

db.create_all()
t_app = app.test_client()


def get_ticket():
    return Ticket.query.filter_by(name=name).first()


def create_ticket():
    t_app.post('/ticket', json={'name': name, 'description': 'description', 'price': '200',
                                'endTimeReservation': '2013-01-12 15:27:43', 'reservationPrice': '100'},
               headers={'Authorization': 'Bearer ' + str(get_token())})


def create_user():
    t_app.post('/user/create', json={'username': 'Nazar', 'email': email, 'password': '123'})


def delete_user():
    t_app.delete('/user/' + str(get_user().id),
                 json={'username': 'Nazar', 'email': email, 'password': '123'},
                 headers={'Authorization': 'Bearer ' + str(get_token())})


def get_reservation(ticket_id):
    return Reservation.query.filter_by(ticket_id=ticket_id).first()


def get_order(ticket_id):
    return Order.query.filter_by(ticket_id=ticket_id).first()


def get_user():
    return User.query.filter_by(email=email).first()


def get_token():
    return dict(t_app.post('/login', json={'username': 'Nazar', 'password': '123'}).json)['access_token']


def test_start():
    create_user()
    create_ticket()
    assert True


def test_show_store_inventory_200():
    data = t_app.get('/store/inventory', json={"status": "available"},
                     headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '200' in str(data)


def test_show_store_inventory_404():
    data = t_app.get('/store/inventory', json={}, headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '404' in str(data)


def test_reservation_store_200():
    data = t_app.post('/store/reservation', json={'ticket_id': str(get_ticket().id)},
                      headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '200' in str(data)


def test_reservation_store_403():
    data = t_app.post('/store/reservation', json={'ticket_id': str(get_ticket().id)},
                      headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '403' in str(data)


def test_reservation_store_404():
    data = t_app.post('/store/reservation', json={'ticket_id': '9999999'},
                      headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '404' in str(data)


def test_reservation_tools_404():
    data = t_app.get('/store/reservation/1', json={}, headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '404' in str(data)


def test_reservation_tools_get_200():
    data = t_app.get('/store/reservation/' + str(get_reservation(get_ticket().id).id),
                     json={'ticket_id': str(get_ticket().id)}, headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '200' in str(data)


def test_order_the_ticket_403():
    create_ticket()
    print(get_ticket().status + '\t' + str(get_ticket().id))
    data = t_app.post('/store/order', json={'ticket_id': str(get_ticket().id)},
                      headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '403' in str(data)


def test_reservation_tools_delete_200():
    data = t_app.delete('/store/reservation/' + str(get_reservation(get_ticket().id).id),
                        json={'ticket_id': str(get_ticket().id)},
                        headers={'Authorization': 'Bearer ' + str(get_token())})
    t_app.delete('/ticket/' + str(get_ticket().id), headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '200' in str(data)


def test_order_the_ticket_404():
    data = t_app.post('/store/order', json={}, headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '404' in str(data)


def test_order_the_ticket_200():
    create_ticket()
    print(get_ticket().status + '\t' + str(get_ticket().id))
    data = t_app.post('/store/order', json={'ticket_id': str(get_ticket().id)},
                      headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '200' in str(data)


def test_order_the_ticket_404_2():
    data = t_app.get('/store/order/99', json={'ticket_id': str(get_ticket().id)},
                     headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '404' in str(data)


def test_order_tools_get_200():
    data = t_app.get('/store/order/' + str(get_order(get_ticket().id).id),
                     json={'ticket_id': str(get_ticket().id)}, headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '200' in str(data)


def test_order_tools_delete_200():
    data = t_app.delete('/store/order/' + str(get_order(get_ticket().id).id),
                        json={'ticket_id': str(get_ticket().id)},
                        headers={'Authorization': 'Bearer ' + str(get_token())})
    t_app.delete('/ticket/' + str(get_ticket().id), headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '200' in str(data)


def test_order_ticket_delete_200():
    data = t_app.delete('/ticket/' + str(get_ticket().id), headers={'Authorization': 'Bearer ' + str(get_token())})
    assert '200' in str(data)


def test_end():
    delete_user()
