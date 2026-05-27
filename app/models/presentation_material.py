from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import db
 
class PresentationMaterial(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    speaker_id: Mapped[int] = mapped_column(ForeignKey('speaker.id'))
    session_id: Mapped[int] = mapped_column(ForeignKey('session.id'))
    file_path: Mapped[str] = mapped_column(String(255))
 
    speaker: Mapped["Speaker"] = relationship(back_populates="materials")
    session: Mapped["Session"] = relationship(back_populates="materials")