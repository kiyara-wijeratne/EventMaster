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