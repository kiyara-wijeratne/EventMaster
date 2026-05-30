from typing import List
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import db
 
class TicketType(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey('event.id'))
    name: Mapped[str] = mapped_column(String(50))
    max_quantity: Mapped[int] = mapped_column(Integer)
    sales_start: Mapped[datetime] = mapped_column(DateTime)
    sales_end: Mapped[datetime] = mapped_column(DateTime)
    price: Mapped[int] = mapped_column(Integer)
 
    event: Mapped["Event"] = relationship(back_populates="ticket_types")
    registrations: Mapped[List["Registration"]] = relationship(back_populates="ticket_type")
    
    @classmethod
    def get_total_tickets_quantity(cls, event_id, exclude_ticket_id=None):
        # calculate the total number of ticket types allocated to an event
        # exclude ticket id so it doesn't count itself during updates
        query = db.select(cls).filter_by(event_id=event_id)
        if exclude_ticket_id:
            query = query.filter(cls.id != exclude_ticket_id)
            
        total_tickets = db.session.execute(query).scalars().all()
        # calculate the sum of all ticket types
        return sum(ticket.max_quantity for ticket in total_tickets if ticket.max_quantity)
        
    @classmethod
    def create(cls, event_id, name, max_quantity, sales_start, sales_end, price):
        # validate ticket sales don't end before they start
        if sales_start >= sales_end:
            raise ValueError("Ticket sales end time must be after the start time.")
        
        # validate ticket sales end before event starts
        from app.models.event import Event
        event = Event.get_by_id(event_id)
        if sales_end >= event.event_start:
            raise ValueError("Ticket sales end time must be before event starts.")
        
        # check sum of ticket type quantities is not more than event capacity
        ticket_type_sum = cls.get_total_tickets_quantity(event_id)
        if ticket_type_sum + max_quantity > event.capacity:
            raise ValueError(f"Cannot allocate {max_quantity} tickets."
                             f"The event only has capacity for {event.capacity - ticket_type_sum} tickets remaining.")
        
        ticket = cls(event_id=event_id,
                     name=name,
                     max_quantity=max_quantity,
                     sales_start=sales_start,
                     sales_end=sales_end,
                     price=price)
        db.session.add(ticket)
        db.session.commit()
        return ticket 
    
    @classmethod
    def get_by_id(cls, id):
        return db.session.get(cls, id)
    
    def update(self, name= None, max_quantity=None, sales_start=None, sales_end=None, price=None):
        from app.models.event import Event
        event = Event.get_by_id(self.event_id)
        
        if name:
            self.name = name
        if max_quantity:
            # check sum of ticket type quantities is not more than event capacity
            ticket_type_sum = self.get_total_tickets_quantity(self.event_id)
            if ticket_type_sum + max_quantity > event.capacity:
                raise ValueError(f"Cannot alloccate {max_quantity} tickets."
                                f"The event only has capacity for {event.capacity - ticket_type_sum} tickets remaining.")
        
        new_start = sales_start or self.sales_start
        new_end = sales_end or self.sales_end
        
        # validate ticket sales don't end before they start
        if new_start >= new_end:
            raise ValueError("Ticket sales end time must be after the start time.")
        # validate ticket sales end before event starts
        if new_end >= event.event_start:
            raise ValueError("Ticket sales end time must be before event starts.")
        
        if sales_start:
            self.sales_start = sales_start
        if sales_end:
            self.sales_end = sales_end
        if price:
            self.price = price
            
        db.session.commit()
        return self
    
    def delete(self):
        # validate no attendees still registered to ticket type
        active_registrations = [registration for registration in self.registrations 
                                if registration.approval_status != "Cancelled"]
        if active_registrations:
            raise ValueError(f"Cannot delete {self.name} ticket."
                             "There are active registrations using it.")
            
        db.session.delete(self)
        db.session.commit()        