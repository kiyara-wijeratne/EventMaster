from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import db
 
class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255))
    role_id: Mapped[int] = mapped_column(ForeignKey('role.id'))
 
    role: Mapped["Role"] = relationship(back_populates="users")
    organised_events: Mapped[List["Event"]] = relationship(back_populates="organiser")
    registrations: Mapped[List["Registration"]] = relationship(back_populates="attendee")
    check_ins_managed: Mapped[List["CheckIn"]] = relationship(back_populates="coordinator")