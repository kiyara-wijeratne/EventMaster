from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import db
 
class CheckIn(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    registration_id: Mapped[int] = mapped_column(ForeignKey('registration.id'))
    coordinator_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
 
    registration: Mapped["Registration"] = relationship(back_populates="check_in")
    coordinator: Mapped["User"] = relationship(back_populates="check_ins_managed")