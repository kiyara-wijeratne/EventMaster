from typing import Optional
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import db
 
class Registration(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey('event.id'))
    ticket_type_id: Mapped[int] = mapped_column(ForeignKey('ticket_type.id'))
    attendee_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    approval_status: Mapped[str] = mapped_column(String(20))
    payment_status: Mapped[str] = mapped_column(String(20))
    special_requests: Mapped[Optional[str]] = mapped_column(Text)
 
    event: Mapped["Event"] = relationship(back_populates="registrations")
    ticket_type: Mapped["TicketType"] = relationship(back_populates="registrations")
    attendee: Mapped["User"] = relationship(back_populates="registrations")
    check_in: Mapped[Optional["CheckIn"]] = relationship(back_populates="registration")
    
    @classmethod
    def create(cls, event_id, ticket_type_id, attendee_id, payment_status, special_requests):
        from app.models.event import Event
        from app.models.user import User
        from app.models.ticket_type import TicketType
        
        # validate event exists
        event = Event.get_by_id(event_id)
        if event is None:
            raise ValueError("Cannot register. The specified event does not exist.")
        
        # validate ticket type exists
        ticket_type = TicketType.get_by_id(ticket_type_id)
        if ticket_type is None:
            raise ValueError("Cannot register. The specifed ticket type does not exist.")
        
        # validate attendee exists
        attendee = User.get_by_id(attendee_id)
        if attendee is None:
            raise ValueError("Cannot register. The specified attendee id does not exist."
                             "Please create an account first.")
        
        # validate ticket belongs to the event 
        if ticket_type.event_id != event_id:
            raise ValueError("Cannot register."
                             f"The {ticket_type.name} does not belong to {event.title}.")
        
        # validate event has capacity for attendee
        if event.has_available_capacity():
            status = "Approved"
        else:
            status = "Waitlisted"
            
        # future scope:
        # validate payment status with third party payment service
            
        registration = cls(event_id=event_id,
                           ticket_type_id=ticket_type_id,
                           attendee_id=attendee_id,
                           payment_status=payment_status,
                           approval_status=status)
        
        db.session.add(registration)
        db.session.commit()
        return registration
    
    @classmethod
    def get_by_id(cls, id):
        return db.session.get(cls, id)
    
    def approve(self):        
        # validate registration not already approved
        if self.approval_status == "Approved":
            return self
        
        # validate event is not at capacity if registration moved to approved  
        from app.models.event import Event
        event = Event.get_by_id(self.event_id)
            
        if not event.has_available_capacity():
            raise ValueError("Cannot approve this registration."
                            f"{event.title} is already at full capacity.")
        
        self.approval_status = "Approved"
        db.session.commit()
        
        # future scope:
        # email attendee to confirm approval
        
        return self
    
    def waitlist(self):
        # validate attendee is not already approved 
        if self.approval_status == "Approved":
            raise ValueError("Cannot waitlist an attendee who is already approved.")
        
        self.approval_status = "Waitlisted"
        db.session.commit()
    
        # future scope:
        # email attendee to confirm waitlist
        
        return self
        
        
    def cancel(self):
        self.approval_status = "Cancelled"
        db.session.commit()
        
        # future scope:
        # email attendee to confirm cancellation
        
        return self 
    
        
        
        
        