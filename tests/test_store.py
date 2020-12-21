from migrate import app, db
from models import *

db.create_all()
t_app = app.test_client()
name = 'test_name'


def get_ticket():
    return Ticket.query.filter_by(name=name).first()


def create_ticket():
    t_app.post('/ticket', json={'name': name, 'description': 'description', 'price': '200',
                                'endTimeReservation': '2013-01-12 15:27:43', 'reservationPrice': '100'})


def delete_ticket():
    t_app.delete('/ticket/' + str(get_ticket().id))


def get_reservation(ticket_id):
    return Reservation.query.filter_by(ticket_id=ticket_id).first()


def get_order(ticket_id):
    return Order.query.filter_by(ticket_id=ticket_id).first()


create_ticket()


def test_show_store_inventory_200():
    data = t_app.get('/store/inventory', json={"status": "available"})
    assert '200' in str(data)


def test_show_store_inventory_404():
    data = t_app.get('/store/inventory', json={})
    assert '404' in str(data)


def test_reservation_store_200():
    data = t_app.post('/store/reservation', json={'ticket_id': str(get_ticket().id)})
    assert '200' in str(data)


def test_reservation_tools_404():
    data = t_app.get('/store/reservation/1', json={})
    assert '404' in str(data)


def test_reservation_tools_get_200():
    data = t_app.get('/store/reservation/' + str(get_reservation(get_ticket().id).id),
                     json={'ticket_id': str(get_ticket().id)})
    assert '200' in str(data)


def test_reservation_tools_delete_200():
    data = t_app.delete('/store/reservation/' + str(get_reservation(get_ticket().id).id),
                        json={'ticket_id': str(get_ticket().id)})
    assert '200' in str(data)


def test_order_the_ticket_404():
    data = t_app.post('/store/order', json={})
    assert '404' in str(data)


def test_order_the_ticket_200():
    delete_ticket()
    create_ticket()
    data = t_app.post('/store/order', json={'ticket_id': str(get_ticket().id)})
    assert '200' in str(data)


def test_order_tools_get_200():
    data = t_app.get('/store/order/' + str(get_order(get_ticket().id).id),
                     json={'ticket_id': str(get_ticket().id)})
    assert '200' in str(data)


def test_order_tools_delete_200():
    data = t_app.delete('/store/order/' + str(get_order(get_ticket().id).id),
                        json={'ticket_id': str(get_ticket().id)})
    assert '200' in str(data)


def test_delete():
    delete_ticket()
    assert True
