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