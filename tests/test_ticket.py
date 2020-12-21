from migrate import app, db
from models import *

db.create_all()
t_app = app.test_client()
name = 'some name'


def get_ticket():
    return Ticket.query.filter_by(name=name).first()


def test_create_ticket_200():
    data = t_app.post('/ticket', json={'name': name, 'description': 'description', 'price': '200',
                                       'endTimeReservation': '2013-01-12 15:27:43', 'reservationPrice': '100'})
    assert '200' in str(data)


def test_create_ticket_204():
    data = t_app.post('/ticket',
                      json={'description': 'description', 'price': '200', 'endTimeReservation': '2013-01-12 15:27:43',
                            'reservationPrice': '100'})
    assert '204' in str(data)


def test_ticket_findByStatus_200():
    data = t_app.get('/ticket/findByStatus', json={'status': 'available'})
    assert '200' in str(data)


def test_ticket_findByStatus_404():
    data = t_app.get('/ticket/findByStatus', json={})
    assert '404' in str(data)


def test_order_ticket_get_200():
    data = t_app.get('/ticket/' + str(get_ticket().id))
    assert '200' in str(data)


def test_order_ticket_get_404():
    data = t_app.get('/ticket/9999')
    assert '404' in str(data)


def test_order_ticket_put_200():
    data = t_app.put('/ticket/' + str(get_ticket().id),
                     json={'name': name, 'description': 'description', 'price': '300',
                           'endTimeReservation': '2013-01-12 15:27:43', 'reservationPrice': '100', 'status': 'end'})
    assert '200' in str(data)


def test_order_ticket_delete_200():
    data = t_app.delete('/ticket/' + str(get_ticket().id))
    assert '200' in str(data)
