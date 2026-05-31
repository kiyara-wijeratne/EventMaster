import pytest
from datetime import datetime

from app.models.event import Event
from app.models.session import Session
from app.models.ticket_type import TicketType
from app.models.role import Role
from app.models.user import User
from app.models.registration import Registration
from app.models.speaker import Speaker
from app.models.presentation_material import PresentationMaterial

@pytest.mark.usefixtures("app_ctx")
class TestWorkshop():
    
    TICKET_SALES_START = datetime(2026, 1, 1, 12, 0)
    TICKET_SALES_END = datetime(2026, 1, 31, 12, 0)
    
    WORKSHOP_START = datetime(2026, 3, 25, 9, 0)
    WORKSHOP_END = datetime(2026, 3, 25, 17, 0)
    
    def test_workshop_session_outside_event_time_raises_value_error(self, seed_workshop_event_type, seed_organiser):
        """
        Test all workshop session fall within event timings.
        """
        
        # arrange
        workshop = Event.create(title="Intro to SQL", 
                                event_type_id=seed_workshop_event_type.id,
                                venue="British Computing Society",
                                capacity=100,
                                event_start=self.WORKSHOP_START, 
                                event_end=self.WORKSHOP_END,
                                organiser_id=seed_organiser.id)
        
        # create a session that starts before the workshop starts
        session_start = datetime(2026, 2, 25, 9, 0)
        session_end = datetime(2026, 2, 25, 12, 0)
        
        # act
        with pytest.raises(ValueError) as error:
            Session.create(event_id=workshop.id,
                           title="Creating a Database",
                           session_start=session_start,
                           session_end=session_end,
                           room="Room 1")
            
        # assert
        assert "Session time must fall within main event hours." in str(error.value)
        
    def test_workshop_manual_approval_overbooking_raises_value_error(self, seed_workshop_event_type, seed_organiser):
        """
        Test manually approval will fail for an attendee on the waitlist
        of an overbooked event. 
        """
        
        # arrange
        workshop = Event.create(title="Python 101", 
                                event_type_id=seed_workshop_event_type.id,
                                venue="NAIC",
                                capacity=1,
                                event_start=self.WORKSHOP_START, 
                                event_end=self.WORKSHOP_END,
                                organiser_id=seed_organiser.id)
        
        ticket = TicketType.create(event_id=workshop.id,
                                   name="General",
                                   max_quantity=1,
                                   sales_start=self.TICKET_SALES_START,
                                   sales_end=self.TICKET_SALES_END,
                                   price=10)
        
        role = Role.create(name="Attendee")
        
        user_one = User.create(email="user_one@test.com",
                               password="password",
                               full_name="User One",
                               role_id=role.id)
        
        user_two = User.create(email="user_two@test.com",
                               password="password",
                               full_name="User Two",
                               role_id=role.id)
        
        # user one registration approved
        user_one_registration = Registration.create(event_id=workshop.id,
                            ticket_type_id=ticket.id,
                            attendee_id=user_one.id,
                            payment_status="Paid",
                            special_requests="")
        
        # user two registration waitlisted 
        user_two_registration = Registration.create(event_id=workshop.id,
                            ticket_type_id=ticket.id,
                            attendee_id=user_two.id,
                            payment_status="Pending",
                            special_requests="")
        
        # act
        with pytest.raises(ValueError) as error:
            user_two_registration.approve()
            
        # assert
        assert "already at full capacity" in str(error.value)
        # validate status did not change
        assert user_two_registration.approval_status == "Waitlisted"
        
    def test_speaker_session_changes_deletes_presentation_materials(self, seed_workshop_event_type, seed_organiser):
        """
        Test presentation materials are deleted if the speaker for a 
        session changes.
        """
        
        # arrange
        workshop = Event.create(title="HTML/CSS", 
                                event_type_id=seed_workshop_event_type.id,
                                venue="Gaydon",
                                capacity=25,
                                event_start=self.WORKSHOP_START, 
                                event_end=self.WORKSHOP_END,
                                organiser_id=seed_organiser.id)
        
        session_start = datetime(2026, 3, 25, 9, 0)
        session_end = datetime(2026, 3, 25, 12, 0)
        
        session = Session.create(event_id=workshop.id,
                                 title="HTML",
                                 session_start=session_start,
                                 session_end=session_end,
                                 room="Auditorium")
        
        speaker = Speaker.create(full_name="Speaker One",
                                 biography="I know everything about web dev!",
                                 email="speaker@test.com",
                                 phone_number="07311225859",
                                 profile_image="speaker.png")
        
        session.add_speaker(speaker.id)
        
        presentation_material = PresentationMaterial.create(speaker_id=speaker.id,
                                                            session_id=session.id,
                                                            file_path="html.ppt")
        
        # validate test setup
        # tests material was linked to session
        assert len(session.materials) == 1
        
        # act
        updated_session = session.remove_speaker(speaker.id)
        
        # assert
        assert len(updated_session.materials) == 0
        assert PresentationMaterial.get_by_id(presentation_material.id) is None
            
        