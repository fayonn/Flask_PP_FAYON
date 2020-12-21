from models import *

# category = Category(name='topClass')
# ticket = Ticket(name='theaterTicket', category=category)
# reservation = Reservation(status='waiting', ticket=ticket, complete=False)
# order = Order(status='placed', ticket=ticket, complete=False)
# user = User(username='user', password='password')
# db.session.add(reservation)
# db.session.add(ticket)
# db.session.add(category)
# db.session.add(user)
# db.session.commit()
db.create_all()
