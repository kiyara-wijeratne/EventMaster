from typing import List, Optional
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import db
from app.models.session_speaker import session_speaker
 
class Speaker(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    biography: Mapped[Optional[str]] = mapped_column(Text)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20))
    profile_image: Mapped[Optional[str]] = mapped_column(String(255))
 
    sessions: Mapped[List["Session"]] = relationship(secondary=session_speaker, back_populates="speakers")
    materials: Mapped[List["PresentationMaterial"]] = relationship(back_populates="speaker")