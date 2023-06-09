from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import Ticket, Passenger, Destination, SeatPreference, Base  # Import your model classes and Base from models.py

engine = create_engine('sqlite:///flights.db')
Base.metadata.create_all(engine)  # Create the tables

Session = sessionmaker(bind=engine)
session = Session()

# Create instances of the model classes and populate them with data
passenger1 = Passenger(name='Johns', contact_details='john@gmail.com', username='john', password='pass123')
passenger2 = Passenger(name='Kate', contact_details='kate@gmail.com', username='kate', password='pass456')
passenger3 = Passenger(name='Michael', contact_details='michael@gmail.com', username='michael', password='pass789')
passenger4 = Passenger(name='Emily', contact_details='emily@gmail.com', username='emily', password='pass012')
passenger5 = Passenger(name='David', contact_details='david@gmail.com', username='david', password='pass345')

destination1 = Destination(location='New York', airport='JFK', availability=10)
destination2 = Destination(location='London', airport='LHR', availability=5)
destination3 = Destination(location='Paris', airport='CDG', availability=7)
destination4 = Destination(location='Tokyo', airport='HND', availability=3)
destination5 = Destination(location='Sydney', airport='SYD', availability=8)

seat_preference1 = SeatPreference(seat_type='Window', seat_class='Economy')
seat_preference2 = SeatPreference(seat_type='Aisle', seat_class='Business')
seat_preference3 = SeatPreference(seat_type='Middle', seat_class='Economy')
seat_preference4 = SeatPreference(seat_type='Window', seat_class='Business')
seat_preference5 = SeatPreference(seat_type='Aisle', seat_class='First Class')

ticket1 = Ticket(passenger=passenger1, destination=destination1, booking_status='Confirmed', seat=seat_preference1)
ticket2 = Ticket(passenger=passenger2, destination=destination2, booking_status='Pending', seat=seat_preference2)
ticket3 = Ticket(passenger=passenger3, destination=destination3, booking_status='Confirmed', seat=seat_preference3)
ticket4 = Ticket(passenger=passenger4, destination=destination4, booking_status='Pending', seat=seat_preference4)
ticket5 = Ticket(passenger=passenger5, destination=destination5, booking_status='Confirmed', seat=seat_preference5)

# Add the instances to the session
session.add_all([
    passenger1, passenger2, passenger3, passenger4, passenger5,
    destination1, destination2, destination3, destination4, destination5,
    seat_preference1, seat_preference2, seat_preference3, seat_preference4, seat_preference5,
    ticket1, ticket2, ticket3, ticket4, ticket5
])

# Commit the changes to the database
session.commit()
