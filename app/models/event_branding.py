from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import db
 
class EventBranding(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey('event.id'))
    logo_path: Mapped[Optional[str]] = mapped_column(String(255))
    primary_colour: Mapped[Optional[str]] = mapped_column(String(7))
    secondary_colour: Mapped[Optional[str]] = mapped_column(String(7))
 
    event: Mapped["Event"] = relationship(back_populates="branding")