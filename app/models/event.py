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
    branding: Mapped[Optional["EventBranding"]] = relationship(back_populates="event")
    ticket_types: Mapped[List["TicketType"]] = relationship(back_populates="event")
    registrations: Mapped[List["Registration"]] = relationship(back_populates="event")
    sessions: Mapped[List["Session"]] = relationship(back_populates="event")