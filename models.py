from migrate import db

Base = db.Model


class Category(db.Model):  # не закрив ticket_controller
    __tablename__ = 'categories'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.VARCHAR(length=40))


class User(db.Model):  # закрив user_controller
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.VARCHAR(length=40), nullable=False)
    email = db.Column('email', db.VARCHAR(30), nullable=False)
    password = db.Column('password', db.VARCHAR(length=120), nullable=False)


class Ticket(db.Model):  # не закрив ticket_controller
    __tablename__ = 'tickets'
    id = db.Column('id', db.Integer, primary_key=True, unique=True)
    name = db.Column('name', db.VARCHAR(length=40), nullable=False)
    description = db.Column('description', db.VARCHAR(length=400))
    price = db.Column('price', db.Integer)
    endTimeReservation = db.Column('endTimeReservation', db.TIMESTAMP)
    reservationPrice = db.Column('reservationPrice', db.Integer)
    status = db.Column('status', db.VARCHAR(20))


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column('id', db.Integer, primary_key=True, unique=True)
    ticket_id = db.Column('ticket_id', db.Integer, db.ForeignKey(Ticket.id), unique=True)
    ticket = db.relationship("Ticket", backref="order")
    status = db.Column('status', db.VARCHAR(20))


class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column('id', db.Integer, primary_key=True, unique=True)
    ticket_id = db.Column('ticket_id', db.Integer, db.ForeignKey(Ticket.id), unique=True)
    ticket = db.relationship("Ticket", backref="reservation")
    status = db.Column('status', db.VARCHAR(20))

