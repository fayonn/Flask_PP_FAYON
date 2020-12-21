from migrate import *
from models import *
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required


def get_current_user():
    return User.query.filter_by(username=get_jwt_identity()).first()


@app.route('/ticket', methods=['POST'])
@jwt_required
def create_ticket():
    name = request.json.get('name', None)
    description = request.json.get('description', None)
    price = request.json.get('price', None)
    endTimeReservation = request.json.get('endTimeReservation', None)
    reservationPrice = request.json.get('reservationPrice', None)
    if name and description and price \
            and endTimeReservation and reservationPrice:
        new_ticket = Ticket(name=name,
                            description=description,
                            price=price,
                            endTimeReservation=endTimeReservation,
                            reservationPrice=reservationPrice,
                            status='available')
        db.session.add(new_ticket)
        db.session.commit()
        return jsonify({"status": 'created', "user_id": get_current_user().id}), 200
    else:
        return jsonify({"status": 'Bad data'}), 204


@app.route('/ticket/findByStatus', methods=['GET'])
@jwt_required
def ticket_findByStatus():
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


@app.route('/ticket/<id>', methods=['PUT', 'GET', 'DELETE'])
@jwt_required
def order_ticket(id):
    ticket = Ticket.query.filter_by(id=id).first()
    if not ticket:
        return jsonify({"msg": "Not Found"}), 404
    if request.method == 'PUT':
        name = request.json.get('name', None)
        description = request.json.get('description', None)
        price = request.json.get('price', None)
        endTimeReservation = request.json.get('endTimeReservation', None)
        reservationPrice = request.json.get('reservationPrice', None)
        status = request.json.get('status', None)

        if name and description and price \
                and endTimeReservation and reservationPrice and status:
            ticket.name = name,
            ticket.description = description,
            ticket.price = price,
            ticket.endTimeReservation = endTimeReservation,
            ticket.reservationPrice = reservationPrice,
            ticket.status = status
            db.session.commit()
            return jsonify({"status": 'updated'}), 200
        else:
            return jsonify({"status": 'Bad data'}), 204
    if request.method == 'GET':
        ticket_ser = {
            "name": ticket.name,
            "description": ticket.description,
            "price": ticket.price,
            "endTimeReservation": ticket.endTimeReservation,
            "reservationPrice": ticket.reservationPrice,
            "status": ticket.status
        }
        return jsonify(ticket_ser), 200
    if request.method == 'DELETE':
        db.session.delete(ticket)
        db.session.commit()
        ticket_ser = {
            "name": ticket.name,
            "description": ticket.description,
            "price": ticket.price,
            "endTimeReservation": ticket.endTimeReservation,
            "reservationPrice": ticket.reservationPrice,
            "status": ticket.status
        }
        return jsonify(ticket_ser), 200
