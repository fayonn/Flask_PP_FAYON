from migrate import *
from flask import request, jsonify
from models import *
from flask_jwt_extended import get_jwt_identity, jwt_required


def get_current_user():
    return User.query.filter_by(username=get_jwt_identity()).first()


@app.route('/store/inventory', methods=['GET'])
@jwt_required
def show_store_inventory():
    status = request.json.get('status', None)
    if not status:
        return jsonify({"msg": "Not Found"}), 404
    tickets = Ticket.query.filter_by(status=status).all()
    ticket_list = {'ticket_list': []}
    for i in tickets:
        ticket_list['ticket_list'].append({'id': i.id, 'name': i.name, 'description': i.description,
                                           'price': i.price, 'endTimeReservation': i.endTimeReservation,
                                           'reservationPrice': i.reservationPrice})

    return jsonify(ticket_list), 200


@app.route('/store/reservation', methods=['POST'])  # створення бронювання
@jwt_required
def reservation_store():
    ticket_id = request.json.get('ticket_id', None)
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    if not ticket:
        return jsonify({"msg": "Not Found"}), 404
    if ticket.status != 'available':
        return jsonify({"msg": "Forbidden"}), 403
    if ticket_id:
        new_reservation = Reservation(ticket=ticket,
                                      ticket_id=ticket_id,
                                      status='waiting')
        ticket.status = 'pending'
        db.session.add(new_reservation)
        db.session.commit()
        return jsonify({"status": 'created'}), 200
    else:
        return jsonify({"status": 'Bad data'}), 204


@app.route('/store/reservation/<id>', methods=['GET', 'DELETE'])  # оновлення
@jwt_required
def reservation_tools(id):
    ticket_id = request.json.get('ticket_id', None)
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    if not ticket:
        return jsonify({"msg": "Not Found"}), 404
    reservation = Reservation.query.filter_by(id=id).first()
    if not reservation:
        return jsonify({"msg": "Not Found"}), 404
    if request.method == 'GET':
        reservation1 = {
            "ticket_id": reservation.ticket_id,
            "status": reservation.status
        }
        return jsonify(reservation1), 200
    if request.method == 'DELETE':
        db.session.delete(reservation)
        reservation.status = 'payed'
        ticket.status = 'sold'
        db.session.commit()
        reservation1 = {
            "ticket_id": reservation.ticket_id,
            "status": reservation.status
        }
        return jsonify(reservation1), 200


@app.route('/store/order', methods=['POST'])
@jwt_required
def order_the_ticket():
    ticket_id = request.json.get('ticket_id', None)
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    if not ticket:
        return jsonify({"msg": "Not Found"}), 404
    if ticket.status != 'available':
        return jsonify({"msg": "Forbidden"}), 403
    if ticket_id:
        new_order = Order(ticket=ticket,
                          ticket_id=ticket_id,
                          status='waiting')
        db.session.add(new_order)
        ticket.status = 'pending'
        db.session.commit()
        return jsonify({"status": 'created'}), 200
    else:
        return jsonify({"status": 'Bad data'}), 204


@app.route('/store/order/<id>', methods=['GET', 'DELETE'])  #
@jwt_required
def order_tools(id):
    ticket_id = request.json.get('ticket_id', None)
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    if not ticket:
        return jsonify({"msg": "Not Found"}), 404
    order = Order.query.filter_by(id=id).first()
    if not order:
        return jsonify({"msg": "Not Found"}), 404
    if request.method == 'GET':
        order1 = {
            "ticket_id": order.ticket_id,
            "status": order.status
        }
        return jsonify(order1), 200
    if request.method == 'DELETE':
        db.session.delete(order)
        order.status = 'payed'
        ticket.status = 'sold'
        db.session.commit()
        order1 = {
            "ticket_id": order.ticket_id,
            "status": order.status
        }
        return jsonify(order1), 200
