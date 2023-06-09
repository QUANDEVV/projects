from os import name
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from prettytable import PrettyTable

engine = create_engine('sqlite:///flights.db')
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class Ticket(Base):
    __tablename__ = 'tickets'

    ticket_id = Column(Integer(), primary_key=True)
    passenger_id = Column(Integer(), ForeignKey('passengers.passenger_id'))
    destination_id = Column(Integer(), ForeignKey('destinations.destination_id'))
    booking_status = Column(String())

    passenger = relationship("Passenger", back_populates="tickets")
    destination = relationship("Destination", back_populates="tickets")
    seat = relationship("SeatPreference", uselist=False, back_populates="ticket")


class Passenger(Base):
    __tablename__ = 'passengers'

    passenger_id = Column(Integer(), primary_key=True)
    name = Column(String())
    contact_details = Column(String())
    username = Column(String(), unique=True)
    password = Column(String())

    tickets = relationship("Ticket", back_populates="passenger")


class Destination(Base):
    __tablename__ = 'destinations'

    destination_id = Column(Integer(), primary_key=True)
    location = Column(String())
    airport = Column(String())
    availability = Column(Integer())

    tickets = relationship("Ticket", back_populates="destination")


class SeatPreference(Base):
    __tablename__ = 'seats'

    seat_id = Column(Integer(), primary_key=True)
    seat_type = Column(String())  # Window, Aisle, Middle
    seat_class = Column(String())  # Economy, Business, First Class
    ticket_id = Column(Integer(), ForeignKey('tickets.ticket_id'))

    ticket = relationship("Ticket", back_populates="seat")


def login():
    print_decorated("LOGIN")
    username = input_decorated("Enter your username: ")
    password = input_decorated("Enter your password: ")

    passenger = session.query(Passenger).filter(Passenger.username == username, Passenger.password == password).first()

    if passenger:
        print("Login successful.\n")
        print("Welcome on Board.\n")

        return passenger
    else:
        print("Invalid username or password.")
        return None


def print_table(headers, data):
    table = PrettyTable(headers)
    for row in data:
        table.add_row(row)
    table.border = True
    table.align = "l"
    print(table)


def print_decorated(text):
    table = PrettyTable([''])
    table.add_row([text])
    table.border = True
    table.header = False
    table.align = 'l'
    return table


def input_decorated(prompt):
    decorated_prompt = print_decorated(prompt)
    return input(str(decorated_prompt))


def main():
    authenticated_passenger = login()

    choice = 0

    while choice != 8:
        print_decorated("*BOOK A PRIVATE JET*")
        print("1. Search for available flights")
        print("2. Book a flight ticket")
        print("3. Cancel a flight ticket")
        print("4. Update a flight ticket")
        print("5. Generate booking history report")
        print("6. Generate popular destinations report")
        print("7. Generate revenue report")
        print("8. Exit")

        choice = int(input_decorated("Enter your choice: "))

        if choice == 1:
            print_decorated("Available flights:\n")
            available_flights = session.query(Destination).filter(Destination.availability > 0).all()

            if available_flights:
                headers = ["Destination", "Airport", "Availability"]
                data = [[flight.location, flight.airport, flight.availability] for flight in available_flights]
                print_table(headers, data)
            else:
                print_decorated("No available flights.")

        elif choice == 2:
            print_decorated("Booking a private jet ticket...")
            destination = input_decorated("Enter the name of the destination: ")
            airport = input_decorated("Enter the destination airport: ")
            passenger_name = input_decorated("Enter your name: ")
            contact_details = input_decorated("Enter your contact details: ")
            seat_type = input_decorated("Enter your seat type preference (Window, Aisle, Middle): ")
            seat_class = input_decorated("Enter your seat class preference (Economy, Business, First Class): ")

            passenger = Passenger(name=passenger_name, contact_details=contact_details)
            seat_preference = SeatPreference(seat_type=seat_type, seat_class=seat_class)
            ticket = Ticket()
            ticket.destination = Destination(location=destination, airport=airport)
            ticket.passenger = passenger
            ticket.seat = seat_preference

            session.add(ticket)
            session.commit()

        elif choice == 3:
            print_decorated("Canceling a flight ticket...")
            ticket_id = int(input_decorated("Enter the ticket ID to cancel: "))
            ticket = session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()

            if ticket:
                ticket.booking_status = "Canceled"
                session.commit()
                print("Ticket canceled successfully.")
            else:
                print_decorated("Ticket not found.")

        elif choice == 4:
            print_decorated("Updating a flight ticket...")
            ticket_id = int(input_decorated("Enter the ticket ID to update: "))

            ticket = session.query(Ticket).get(ticket_id)

            if ticket:
                destination = input_decorated("Enter the new destination: ")
                airport = input_decorated("Enter the new destination airport: ")
                passenger_name = input_decorated("Enter the new passenger name: ")
                contact_details = input_decorated("Enter the new contact details: ")
                seat_type = input_decorated("Enter the new seat type preference (Window, Aisle, Middle): ")
                seat_class = input_decorated("Enter the new seat class preference (Economy, Business, First Class): ")

                ticket.destination.location = destination
                ticket.destination.airport = airport
                ticket.passenger.name = passenger_name
                ticket.passenger.contact_details = contact_details
                ticket.seat.seat_type = seat_type
                ticket.seat.seat_class = seat_class

                session.commit()
                print("Ticket updated successfully.")
            else:
                print_decorated("Ticket not found.")

        elif choice == 5:
            print_decorated("Generating booking history report...")
            bookings = session.query(Ticket).all()

            if bookings:
                headers = ["Passenger", "Destination", "Status"]
                data = [[booking.passenger.name, booking.destination.location, booking.booking_status] for booking in
                        bookings]
                print_table(headers, data)
            else:
                print_decorated("No bookings found.")

        elif choice == 6:
            print_decorated("Generating popular destinations report...")
            destinations = session.query(Destination).order_by(Destination.availability.desc()).limit(5)

            if destinations:
                headers = ["Destination", "Availability"]
                data = [[destination.location, destination.availability] for destination in destinations]
                print_table(headers, data)
            else:
                print_decorated("No destinations found.")

        elif choice == 7:
            print_decorated("Generating revenue report...")
            revenue = session.query(Destination.location, Destination.availability).join(Ticket).filter(
                Ticket.booking_status == "Confirmed").all()

            total_revenue = 0

            if revenue:
                headers = ["Destination", "Revenue"]
                data = []
                for destination in revenue:
                    rev = destination.availability * 1000
                    total_revenue += rev
                    data.append([destination.location, rev])
                print_table(headers, data)

                print_decorated(f"Total Revenue: {total_revenue}")
            else:
                print_decorated("No revenue data found.")

        elif choice == 8:
            print_decorated("Quitting Program")

    session.close()


if __name__ == "__main__":
    Base.metadata.create_all(engine)  # Create tables if they don't exist
    main()
