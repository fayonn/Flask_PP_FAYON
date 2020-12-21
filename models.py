from migrate import db

Base = db.Model


class Category(db.Model):  # не закрив ticket_controller
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(length=40))


class User(db.Model):  # закрив user_controller
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(length=40), nullable=False)
    email = db.Column(db.VARCHAR(30), nullable=False)
    password = db.Column(db.VARCHAR(128), nullable=False)


class Ticket(db.Model):  # не закрив ticket_controller
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.VARCHAR(length=40), nullable=False)
    description = db.Column(db.VARCHAR(length=400))
    price = db.Column(db.Integer)
    endTimeReservation = db.Column(db.TIMESTAMP)
    reservationPrice = db.Column(db.Integer)
    status = db.Column(db.VARCHAR(20))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey(Ticket.id), unique=True)
    ticket = db.relationship("Ticket", backref="order")
    status = db.Column(db.VARCHAR(20))


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey(Ticket.id), unique=True)
    ticket = db.relationship("Ticket", backref="reservation")
    status = db.Column(db.VARCHAR(20))

