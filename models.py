from migrate import db

Base = db.Model


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.VARCHAR(length=40))


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.VARCHAR(length=40), nullable=False)
    password = db.Column('password', db.VARCHAR(length=40), nullable=False)


class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column('id', db.Integer, primary_key=True, unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id))
    category = db.relationship('Category', backref=db.backref("category"))
    name = db.Column('name', db.VARCHAR(length=40), nullable=False)
    description = db.Column('description', db.VARCHAR(length=400))
    price = db.Column('price', db.Integer)
    endTimeReservation = db.Column('endTimeReservation', db.TIMESTAMP)
    reservationPrice = db.Column('reservationPrice', db.Integer)
    status = db.Enum('available', 'pending', 'sold', 'reserved')


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column('id', db.Integer, primary_key=True, unique=True)
    ticket_id = db.Column('ticket_id', db.Integer, db.ForeignKey(Ticket.id), unique=True)
    ticket = db.relationship("Ticket", backref="order")
    status = db.Enum('placed', 'payed')
    complete = db.Column('complete', db.Boolean)


class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column('id', db.Integer, primary_key=True, unique=True)
    ticket_id = db.Column('ticket_id', db.Integer, db.ForeignKey(Ticket.id), unique=True)
    ticket = db.relationship("Ticket", backref="reservation")
    status = db.Enum('waiting', 'payed')
    complete = db.Column('complete', db.Boolean)


class ApiResponse(db.Model):
    __tablename__ = 'apiResponse'
    id = db.Column('id', db.Integer, primary_key=True)
    type = db.Column('type', db.VARCHAR(length=40))
    message = db.Column('message', db.VARCHAR(length=40))

