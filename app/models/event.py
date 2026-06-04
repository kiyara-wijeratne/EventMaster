from typing import List, Optional
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import db
 
class Event(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    event_type_id: Mapped[int] = mapped_column(ForeignKey('event_type.id'))
    venue: Mapped[str] = mapped_column(String(255))
    capacity: Mapped[int] = mapped_column(Integer)
    event_start: Mapped[datetime] = mapped_column(DateTime)
    event_end: Mapped[datetime] = mapped_column(DateTime)
    organiser_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
 
    event_type: Mapped["EventType"] = relationship(back_populates="events")
    organiser: Mapped["User"] = relationship(back_populates="organised_events")
    branding: Mapped[Optional["EventBranding"]] = relationship(back_populates="event", cascade="all, delete-orphan")
    ticket_types: Mapped[List["TicketType"]] = relationship(back_populates="event", cascade="all, delete-orphan")
    registrations: Mapped[List["Registration"]] = relationship(back_populates="event")
    sessions: Mapped[List["Session"]] = relationship(back_populates="event", cascade="all, delete-orphan")
    
    @classmethod
    def create(cls, title, event_type_id, venue, capacity, event_start, event_end, organiser_id):
        # validate event doesn't end before it starts
        if event_start >= event_end:
            raise ValueError("Event end time must be after the start time.")
        
        event = cls(title=title,
                    event_type_id=event_type_id,
                    venue=venue,
                    capacity=capacity,
                    event_start=event_start,
                    event_end=event_end,
                    organiser_id=organiser_id)
        db.session.add(event)
        db.session.commit()
        return event
    
    @classmethod
    def get_by_id(cls, id):
        return db.session.get(cls, id)
    
    def update(self, title=None, venue=None, capacity=None):
        # update basic event details
        if title:
            self.title = title
        if venue:
            self.venue = venue
        if capacity:
            # get all ticket types linked to event
            from app.models.ticket_type import TicketType
            tickets = db.session.execute(db.select(TicketType).filter_by(event_id=self.id)).scalars().all()
            # calculate the total number of ticket types allocated to an event
            tickets_quantity_sum = sum(ticket.max_quantity for ticket in tickets if ticket.max_quantity)
            
            # validate capacity is not less than tickets already allocated
            if capacity < tickets_quantity_sum:
                raise ValueError(f"Cannot reduce capacity to {capacity}."
                                 f"You have already allocated {tickets_quantity_sum} across your ticket types."
                                 "Please reduce ticket allocation first.")
            
            self.capacity = capacity
            
        db.session.commit()
        return self 
    
    def reschedule(self, new_start, new_end):
        # update event_start and event_end details
        if new_start >= new_end:
            raise ValueError("Event end time must be after the start time.")
        
        # validate sessions fall within new event timings
        conflicting_sessions = [
            session.title for session in self.sessions
            if session.session_start < new_start or
            session.session_end > new_end]
        
        if conflicting_sessions:
            names = ",".join(conflicting_sessions)
            raise ValueError(f"Cannot reschedule. The following sessions fall outside the new event schedule: {names}."
                             "Please update those sessions first.")
            
        self.event_start = new_start
        self.event_end = new_end
        db.session.commit()
        return self
        
    def has_available_capacity(self):
        # validate no. approved attendees does not exceed capacity
        approved_registrations = [registration for registration in self.registrations 
                                if registration.approval_status == "Approved"]
        return len(approved_registrations) < self.capacity
    
    def delete(self):
        # validate no attendees still registered to event
        active_registrations = [registration for registration in self.registrations 
                                if registration.approval_status != "Cancelled"]
        
        if active_registrations:
            raise ValueError("Cannot delete event."
                             f"There are {len(active_registrations)} active registrations to it."
                             "You must cancel all attendee registrations before deleting the event.")
            
        db.session.delete(self)
        db.session.commit()