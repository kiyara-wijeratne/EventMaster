from typing import List
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import db
from app.models.session_speaker import session_speaker
 
class Session(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey('event.id'))
    title: Mapped[str] = mapped_column(String(150))
    session_start: Mapped[datetime] = mapped_column(DateTime)
    session_end: Mapped[datetime] = mapped_column(DateTime)
    room: Mapped[str] = mapped_column(String(100))
 
    event: Mapped["Event"] = relationship(back_populates="sessions")
    speakers: Mapped[List["Speaker"]] = relationship(secondary=session_speaker, back_populates="sessions")
    materials: Mapped[List["PresentationMaterial"]] = relationship(back_populates="session")