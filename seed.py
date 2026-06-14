from datetime import datetime

from app import create_app
from app.models import db
from app.models.event import Event
from app.models.event_type import EventType
from app.models.presentation_material import PresentationMaterial
from app.models.registration import Registration
from app.models.role import Role
from app.models.session import Session
from app.models.speaker import Speaker
from app.models.ticket_type import TicketType
from app.models.user import User


def seed_db(app):
    """Seed database with inital data."""

    with app.app_context():

        # creat clean database

        db.drop_all()
        db.create_all()

        # create roles
        administrator = Role.create(name="Administrator")
        organiser = Role.create(name="Organiser")
        coordinator = Role.create(name="Coordinator")
        attendee = Role.create(name="Attendee")

        # create staff users
        admin_user = User.create(
            email="admin@eventmaster.com",
            password="admin",
            full_name="Admin User",
            role_id=administrator.id,
        )

        org_user = User.create(
            email="organiser@eventmaster.com",
            password="organiser",
            full_name="Organiser User",
            role_id=organiser.id,
        )

        coord_user = User.create(
            email="coordinator@eventmaster.com",
            password="coordinator",
            full_name="Coordinator User",
            role_id=coordinator.id,
        )

        # create attendees
        attendee_1 = User.create(
            email="harry@test.com",
            password="password",
            full_name="Harry Cook",
            role_id=attendee.id,
        )

        attendee_2 = User.create(
            email="john@test.com",
            password="password",
            full_name="John Doe",
            role_id=attendee.id,
        )

        attendee_3 = User.create(
            email="han@test.com",
            password="password",
            full_name="Han Lee",
            role_id=attendee.id,
        )

        attendee_4 = User.create(
            email="diana@test.com",
            password="password",
            full_name="Diana Prince",
            role_id=attendee.id,
        )

        # create workshop event type
        workshop = EventType.create(name="Workshop")

        # create events
        event_1 = Event.create(
            title="Python 101",
            event_type_id=workshop.id,
            venue="NAIC",
            capacity=2,
            event_start=datetime(2026, 3, 25, 9, 0),
            event_end=datetime(2026, 3, 25, 17, 0),
            organiser_id=org_user.id,
        )

        event_2 = Event.create(
            title="Intro to SQL",
            event_type_id=workshop.id,
            venue="BCS",
            capacity=3,
            event_start=datetime(2027, 3, 25, 9, 0),
            event_end=datetime(2027, 3, 25, 17, 0),
            organiser_id=org_user.id,
        )

        # add sessions
        session_1 = Session.create(
            event_id=event_2.id,
            title="Creating a Database",
            session_start=datetime(2027, 3, 25, 9, 30),
            session_end=datetime(2027, 3, 25, 12, 30),
            room="Room 1",
        )

        session_2 = Session.create(
            event_id=event_2.id,
            title="Querying",
            session_start=datetime(2027, 3, 25, 13, 0),
            session_end=datetime(2027, 3, 25, 16, 00),
            room="Room 2",
        )

        # add speakers
        speaker_1 = Speaker.create(
            full_name="Alice Holtman",
            biography="I know all about SQL!",
            email="alice@gmail.com",
            phone_number="07311225958",
            profile_image="alice.png",
        )

        speaker_2 = Speaker.create(
            full_name="Dr. Frost",
            biography="I love maths.",
            email="dr.frost@gmail.com",
            phone_number="07311225859",
            profile_image="frost.png",
        )

        # add speaker to session
        session_1.add_speaker(speaker_id=speaker_1.id)

        # add presentation materials
        material_1 = PresentationMaterial.create(
            speaker_id=speaker_1.id, session_id=session_1.id, file_path="databases.ppt"
        )

        # create tickets
        ticket_1 = TicketType.create(
            event_id=event_1.id,
            name="Early Bird",
            price=15,
            max_quantity=1,
            sales_start=datetime(2026, 2, 25, 12, 0),
            sales_end=datetime(2026, 3, 4, 12, 0),
        )

        ticket_2 = TicketType.create(
            event_id=event_1.id,
            name="General Admission",
            price=20,
            max_quantity=1,
            sales_start=datetime(2026, 3, 4, 12, 0),
            sales_end=datetime(2026, 3, 18, 12, 0),
        )

        ticket_3 = TicketType.create(
            event_id=event_2.id,
            name="Standard",
            price=30,
            max_quantity=3,
            sales_start=datetime(2027, 3, 4, 12, 0),
            sales_end=datetime(2027, 3, 18, 12, 0),
        )

        # create registrations event_1
        Registration.create(
            event_id=event_1.id,
            ticket_type_id=ticket_1.id,
            attendee_id=attendee_1.id,
            payment_status="Paid",
            special_requests="Needs wheelchair access",
        )  # approved

        Registration.create(
            event_id=event_1.id,
            ticket_type_id=ticket_2.id,
            attendee_id=attendee_2.id,
            payment_status="Paid",
            special_requests="",
        )  # approved

        Registration.create(
            event_id=event_1.id,
            ticket_type_id=ticket_1.id,
            attendee_id=attendee_3.id,
            payment_status="Pending",
            special_requests="",
        )  # waitlisted

        Registration.create(
            event_id=event_1.id,
            ticket_type_id=ticket_1.id,
            attendee_id=attendee_4.id,
            payment_status="Pending",
            special_requests="",
        )  # waitlisted

        # create registration event_2

        Registration.create(
            event_id=event_2.id,
            ticket_type_id=ticket_3.id,
            attendee_id=attendee_1.id,
            payment_status="Paid",
            special_requests="Needs wheelchair access",
        )  # approved

        Registration.create(
            event_id=event_2.id,
            ticket_type_id=ticket_3.id,
            attendee_id=attendee_2.id,
            payment_status="Paid",
            special_requests="",
        )  # approved

        Registration.create(
            event_id=event_2.id,
            ticket_type_id=ticket_3.id,
            attendee_id=attendee_3.id,
            payment_status="Pending",
            special_requests="",
        )  # approved

        Registration.create(
            event_id=event_2.id,
            ticket_type_id=ticket_3.id,
            attendee_id=attendee_4.id,
            payment_status="Pending",
            special_requests="",
        )  # waitlisted

        print("database seeded")


if __name__ == "__main__":

    app = create_app(config_filename="app.config.DevelopmentConfig")

    seed_db(app)
